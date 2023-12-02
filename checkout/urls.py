from django.urls import path
from.import views

app_name = "checkout"

urlpatterns=[
    path("api", views.CheckoutAPIView.as_view(), name="checkout_view"),
    path("session/api", views.WebhookAPI.as_view(), name="checkout_webhook"),
    path("api/session/status", views.CheckOutStatus().as_view(), name="checkout_status"),
]