from django.urls import path, include
from rest_framework import routers
from .views import TagModelViewSet, FilterModelViewSet, CarrierModelViewSet, CustomerModelViewSet, CampaignModelViewSet, EmailModelViewSet, AllEmailReportAPIView

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
] + router.urls
