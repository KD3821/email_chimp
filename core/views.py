from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Carrier, Tag, Filter, Customer, Campaign, Email
from .serializers import CarrierSerializer, TagSerializer, FilterSerializer, CustomerSerializer, CampaignSerializer,\
    EmailSerializer, ReportEmailsSerializer, SendEmailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .reports import all_emails_report
from datetime import datetime, timedelta
from time import sleep
from .use_requests import use_requests
from .tasks import send_emails_task

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
auth = {'Authorization': 'Bearer ' + api_key}


class CarrierModelViewSet(ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer


class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FilterModelViewSet(ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer


class CustomerModelViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CampaignModelViewSet(ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    filter_backends = [OrderingFilter]

    def list_customers(self, request):
        customer_filter = Filter.objects.filter(slug=request.data['email_filter'])[0:1].get()
        customer_carrier = customer_filter.mobile
        customer_tag = customer_filter.tag
        if customer_tag:
            customer_list = Customer.objects.filter(carrier=customer_carrier).filter(tag=customer_tag).values()
        else:
            customer_list = Customer.objects.filter(carrier=customer_carrier).values()
        print(customer_list)
        return customer_list

    def get_emails(self, request, id_of_camp):
        present = datetime.now()
        start_campaign = datetime.strptime(request.data['date_start'], '%Y-%m-%dT%H:%M:%SZ')
        finish_campaign = datetime.strptime(request.data['date_finish'], '%Y-%m-%dT%H:%M:%SZ')
        if start_campaign <= present < finish_campaign:
            mailing_list = self.list_customers(request)
            msg_list = []
            for obj in mailing_list.values():
                data = {}
                campaign_id = id_of_camp
                customer_id = obj['id']
                data['campaign_id'] = campaign_id
                data['customer_id'] = customer_id
                serializer = SendEmailSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    msg_list.append(serializer.data)
            print(msg_list)
        elif present < start_campaign:
            print("too early!")  # set task for celery
        else:
            print("too late!")  # reply with Error phrase
        pass

    def send_emails(self, request, id_of_camp):
        msgs_list = Email.objects.filter(campaign_id=id_of_camp).select_related('customer_id')
        msg_list = msgs_list.values()
        print(msg_list)
        for msg in msg_list:
            sleep(2)
            print('спим')
            sleep(2)
            print('идем на API')
            sleep(2)
            if msg['is_ok'] == False:
                msg_tmp={}
                msg_tmp['id'] = msg['id']
                msg_tmp['text'] = request.data['text']
                q_msg = msgs_list.get(id=msg['id'])
                msg_tmp['phone'] = int(q_msg.customer_id.phone)
                api_url = 'https://probe.fbrq.cloud/v1/send/{}'.format(msg_tmp['id'])
                r = use_requests(api_url, msg_tmp, auth)
                print(r.status_code)
                sleep(2)
                print('спим')
                sleep(2)
                if r.ok:
                    ok_data = {}
                    ok_data['is_ok'] = True
                    ok_data['campaign_id'] = msg['campaign_id_id']
                    ok_data['customer_id'] = msg['customer_id_id']
                    serializer = SendEmailSerializer(q_msg, data=ok_data)
                    if serializer.is_valid():
                        serializer.save()
                        print('отправлено №' + str(msg_tmp['id']))
                        print(serializer.data)
                        sleep(2)
                        print('спим еще')
                        sleep(2)
                    else:
                        print('не валидно')  # raise ValidationError
                else:
                    print('Не дошло')  # set task for celery
        pass

    def create(self, request, *args, **kwargs):
        request.data['text'] = request.data['text']
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.list_customers(request)
            print(serializer.data['id'])
            self.get_emails(request, serializer.data['id'])
            # self.send_emails(request, serializer.data['id'])  # used for synchronous task
            send_emails_task.delay(serializer.data['id'], request.data['text'])  # used for celery - request is removed, text is passed explicitly
        return Response(serializer.data)


class EmailModelViewSet(ModelViewSet):
    queryset = Email.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["campaign_id__id"]  # to make query with ?campaign_id__id=3

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EmailSerializer
        return SendEmailSerializer


class AllEmailReportAPIView(APIView):
    def get(self, request):
        data = all_emails_report()
        serializer = ReportEmailsSerializer(instance=data, many=True)
        return Response(data=serializer.data)
