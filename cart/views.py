from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, Cart
from .serializers import CartItemSerializer

class CartCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Get the user's cart or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(customer=request.user)

        if cart:
            cart_items = [
                {
                    "id":item.food_item.id,
                    "cart_id":item.id,
                    "name":item.food_item.name, 
                    "image_url":item.food_item.image_url, 
                    "price":item.food_item.price,
                    "quantity":item.quantity
                }
                    for item in CartItem.objects.filter(cart=cart)
            ]
        else:
            cart_items = []
        return Response(cart_items, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # Get the user's cart or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(customer=request.user)
        
        # Create a cart item serializer instance with request data
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the cart item already exists for this food item
            print(serializer.validated_data['food_item'])
            # remember: we are checking with FoodItem id not cart id. 
            existing_item = CartItem.objects.filter(food_item_id=serializer.validated_data['food_item']).first()
            
            if existing_item:
                # Update the quantity if the item already exists
                existing_item.quantity = serializer.validated_data['quantity']
                existing_item.save()
            else:
                # Create a new cart item and associate it with the user's cart
                cart_item = serializer.save(cart=cart)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, *args, **kwargs):
    #     category = get_object_or_404(CartItem)
    #     category.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)