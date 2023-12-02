from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem

# Create your views here.

class OrderListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.is_vendor:
            orders = Order.objects.filter(vendor=request.user)
        else:
            orders = Order.objects.filter(customer=request.user)
        if len(orders) != 0:
            user_orders = [
                {
                    "id":order.id,
                    "total":order.total_amount,
                    "status":order.status,
                    "display_id":order.display_id,
                    "payment_status":order.payment_status,
                    "shipping_charges":1000,
                    "platform_fee":300,
                    "tax_and_gst":500,
                    "tax_percentage":"5%",
                    "vendor":{
                        "id":order.vendor.id,
                        "name":f'{order.vendor.first_name} {order.vendor.last_name}',
                        "phone":order.vendor.get_user_phone()
                    },
                    "customer":{
                        "id":order.customer.id,
                        "name":f'{order.customer.first_name} {order.customer.last_name}',
                        "phone":order.customer.get_user_phone()

                    },
                    "line_items":order.get_serialize_items()
                }
                for order in orders
            ]
            return Response({"orders":user_orders}, status=status.HTTP_200_OK)
        else:
            return Response({"orders":[]}, status=status.HTTP_200_OK)
    
        
        



        
