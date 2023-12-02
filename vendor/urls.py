from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('api/list', views.VendorListAPIView().as_view(), name='vendor_list_api'),
    path('api/<uuid:user_id>/profile', views.VendorAPIView().as_view(), name='vendor_api'),
    path('api/opening/hour', views.TimingAPIView().as_view(), name='vendor_timing'),
]