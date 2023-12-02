from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import CartItem, Cart

class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('food_item', 'quantity')


class CartSerializer(ModelSerializer):
    cart_items = SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'cart_items')

    def get_cart_items(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)        
        cart_items_data = [{'id': item.id, "name":item.name, "image_url":item.image_url, 'quantity': item.quantity} for item in cart_items]
        return cart_items_data