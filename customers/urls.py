from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('api/<uuid:user_id>/profile', views.CustomerAPIView().as_view(), name='customer_api'),
]