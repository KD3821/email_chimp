from django.urls import path, include
from rest_framework import routers
from .views import TagModelViewSet, FilterModelViewSet, CarrierModelViewSet, CustomerModelViewSet, CampaignModelViewSet, EmailModelViewSet, AllEmailReportAPIView,\
    ApiRoot, EmailList, EmailDetail, CustomerList, CustomerDetail, CampaignList, CampaignDetail

router = routers.SimpleRouter()

router.register(r'tags', TagModelViewSet, basename='tags')
router.register(r'filters', FilterModelViewSet, basename='filters')
router.register(r'carriers', CarrierModelViewSet, basename='carriers')
router.register(r'customers', CustomerModelViewSet, basename='customers')
router.register(r'campaigns', CampaignModelViewSet, basename='campaigns')
router.register(r'emails', EmailModelViewSet, basename='emails')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('report_all/', AllEmailReportAPIView.as_view(), name='report'),
    path('__debug__/', include('debug_toolbar.urls')),

    path('new_emails/', EmailList.as_view(), name='email-list'),
    path('new_emails/<int:pk>/', EmailDetail.as_view(), name='email-detail'),
    path('new_customers/', CustomerList.as_view(), name='customer-list'),
    path('new_customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('new_campaigns/', CampaignList.as_view(), name='campaign-list'),
    path('new_campaigns/<int:pk>/', CampaignDetail.as_view(), name='campaign-detail'),
    path('new/', ApiRoot.as_view(), name=ApiRoot.name)

] + router.urls