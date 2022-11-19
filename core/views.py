from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Carrier, Tag, Filter, Customer, Campaign, Email
from .serializers import CarrierSerializer, TagSerializer, FilterSerializer, CustomerSerializer, CampaignSerializer, EmailSerializer, ReportEmailsSerializer, SendEmailSerializer,\
    NewEmailSerializer, NewCustomerSerializer, NewCampaignSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .reports import all_emails_report




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


class EmailModelViewSet(ModelViewSet):
    queryset = Email.objects.all()
    # serializer_class = EmailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["campaign_id__id"]  # to make query with ?campaign_id__id=3

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EmailSerializer
        return SendEmailSerializer

############

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'newcustomers': reverse(CustomerList.name, request=request),
            'newcampaigns': reverse(CampaignList.name, request=request),
            'newemails': reverse(EmailList.name, request=request),
            })

class CustomerList(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = NewCustomerSerializer
    name = 'customer-list'

class CustomerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = NewCustomerSerializer
    name = 'customer-detail'

class CampaignList(ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = NewCampaignSerializer
    name = 'campaign-list'

class CampaignDetail(RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = NewCampaignSerializer
    name = 'campaign-detail'

class EmailList(ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = NewEmailSerializer
    name = 'email-list'

class EmailDetail(RetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = NewEmailSerializer
    name = 'email-detail'

############

class AllEmailReportAPIView(APIView):
    def get(self, request):
        data = all_emails_report()
        serializer = ReportEmailsSerializer(instance=data, many=True)
        return Response(data=serializer.data)


