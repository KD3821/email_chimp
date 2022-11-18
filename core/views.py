from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Carrier, Tag, Filter, Customer, Campaign, Email
from .serializers import CarrierSerializer, TagSerializer, FilterSerializer, CustomerSerializer, CampaignSerializer, EmailSerializer, ReportEmailsSerializer
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
    serializer_class = EmailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["campaign_id__id"]  # to make query with ?campaign_id__id=3


class AllEmailReportAPIView(APIView):
    def get(self, request):
        data = all_emails_report()
        serializer = ReportEmailsSerializer(instance=data, many=True)
        return Response(data=serializer.data)


