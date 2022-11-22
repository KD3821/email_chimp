from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Carrier, Tag, Filter, Customer, Campaign, Email
from .serializers import CarrierSerializer, TagSerializer, FilterSerializer, CustomerSerializer, CampaignSerializer,\
    EmailSerializer, ReportEmailsSerializer, SendEmailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .reports import all_emails_report
from datetime import datetime
from .tasks import send_emails_task
from .utils import get_sec




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
        if customer_list:
            return list(customer_list)
        pass

    def get_emails(self, request, id_of_camp, text_of_camp):
        present = datetime.now()
        start_campaign = datetime.strptime(request.data['date_start'], '%Y-%m-%dT%H:%M:%SZ')
        finish_campaign = datetime.strptime(request.data['date_finish'], '%Y-%m-%dT%H:%M:%SZ')
        if start_campaign <= present < finish_campaign:
            delta_left = finish_campaign - present
            time_left = get_sec(str(delta_left))
            mailing_list = self.list_customers(request)
            if mailing_list:
                send_emails_task.apply_async(args=[id_of_camp, text_of_camp, finish_campaign, mailing_list], expires=time_left)
            else:
                print("нет клиентов")
                return
        elif present < start_campaign:
            delta_left = finish_campaign - present
            delta_before = start_campaign - present
            time_left = get_sec(str(delta_left))
            time_before = get_sec(str(delta_before))
            mailing_list = self.list_customers(request)
            if mailing_list:
                send_emails_task.apply_async(args=[id_of_camp, text_of_camp, finish_campaign, mailing_list], countdown=time_before, expires=time_left)
            else:
                print("нет клиентов")
                return
        else:
            print("too late!")
        pass

    def create(self, request, *args, **kwargs):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.get_emails(request, serializer.data['id'], serializer.data['text'])
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
