from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer
from django.shortcuts import get_object_or_404

class CartItemListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart__customer=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item = serializer.save(cart__customer=request.user)
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
