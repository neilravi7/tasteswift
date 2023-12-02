from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('api/list', views.OrderListAPIView().as_view(), name='orders'),
]