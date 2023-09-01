from rest_framework.serializers import ModelSerializer
from .models import CartItem, Cart


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('id',)