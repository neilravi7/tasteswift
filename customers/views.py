from django.shortcuts import render
from .models import Customer
from .serializers import CustomerSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from location.models import Address

# Create your views here.

class CustomerAPIView(APIView):
    def get_object(self, user_id):
        print("user_id: ", user_id)
        try:
            return Customer.objects.get(user__id=user_id)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        customer = self.get_object(user_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, user_id):
        customer = self.get_object(user_id)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Saving user.first_name and last_name.
            # This thing can be done with signal will be implemented
            user = customer.user
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.save()
            
            address_instance = Address.objects.get_or_create(user=user)[0]
            address_instance.address = request.data.get('address')
            address_instance.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
