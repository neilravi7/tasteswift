import stripe
import json
import random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework .permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from django.conf import settings

# Create your views here.
def generate_unique_display_id():
    while True:
        # Generate a random 10-digit number
        display_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        
        # Check if the generated display_id is unique
        if not Order.objects.filter(display_id=display_id).exists():
            return display_id

class CheckoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def create_order(self, request, cart_items):
        # Get an unique id which is an 10 digit number
        display_id = generate_unique_display_id()
        # create an order instance
        order_instance = Order.objects.create(
            customer=request.user,
            total_amount=0,
            display_id=display_id,
            payment_status="unpaid"
        )
        
        vendor=None
        total_amount=0      
        DELIVERY_CAHRGES=10
        TAX_PERCENTAGE=8

        # create orders items 
        for item in cart_items:
            OrderItem.objects.create(
                order=order_instance,
                food_item=item.food_item,
                quantity=item.quantity
            )

            total_amount += item.food_item.price * item.quantity
            vendor=item.food_item.vendor
        
        tax = (total_amount*TAX_PERCENTAGE)/100
        total_amount = total_amount+tax+DELIVERY_CAHRGES
        order_instance.vendor=vendor
        order_instance.total_amount=total_amount
        order_instance.save()
        return display_id, order_instance

    def post(self, request, *args, **kwargs):
        cart_items = request.user.get_cart_item()
        
        if len(cart_items) == 0:
            return Response({"msg":"Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            line_items = [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.food_item.name,
                            "images":[item.food_item.image_url],
                        },
                        "unit_amount": int(item.food_item.price),
                    },
                    "quantity": item.quantity,
                }
                for item in cart_items
            ]

            # adding extra items as product.
            # We can add tax and shipping ids into stripe but its done for now.
            # Tax an Restaurent Charges
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Tax and Restaurants Fee",
                            "images":["https://cdn-icons-png.flaticon.com/128/3257/3257473.png"],
                        },
                        "unit_amount":1000,
                    },
                    "quantity": 1,
                }
            )

            # Delivery Charges
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Delivery Charges",
                            "images":["https://cdn-icons-png.flaticon.com/128/3063/3063822.png"],
                        },
                        "unit_amount":800,
                    },
                    "quantity": 1,
                }
            )

            stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
            # Create a Stripe Checkout Session
            display_id, order = self.create_order(request, cart_items)
            
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"http://localhost:3000/app/payment/success?order_id={display_id}",
                cancel_url=f"http://localhost:3000/app/payment/success?order_id={display_id}"
            )
            order.stripe_checkout_id=checkout_session.id
            order.save()
            # Clear Cart
            cart_items.delete()  
            return Response({"checkout_url":checkout_session.url, "session_id":checkout_session.id}, status=status.HTTP_200_OK)

class CheckOutStatus(APIView):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
        order_id = request.data.get('order_id')
        order = Order.objects.filter(display_id=order_id).first()
        order_items = order.get_order_items()       
        try:
            checkout_session = stripe.checkout.Session.retrieve(order.stripe_checkout_id)
            checkout_session_data = json.loads(checkout_session.last_response.body)
            order.payment_status = checkout_session_data.get('payment_status')
            if checkout_session_data.get('payment_status') != "paid":
                order.status='canceled'
            else:
                order.status='accepted'
            order.save()

            if order.status == 'canceled':
               success=False
            else:
               success=True

            order={
                "customer_detail":checkout_session_data.get('customer_details'),
                "order_status":order.status
            }

            return Response(
                {
                    "success":success, 
                    "order":order, 
                    "payment_status":checkout_session_data.get('payment_status')
                }, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"success":False, "error":str(e)}, status=status.HTTP_200_OK)





# Webhook to trace checkout
# settings.STRIPE_API_KEY_HIDDEN
# settings.STRIPE_API_KEY_PUBLISHABLE
# settings.STRIPE_ENDPOINT_SECRET

class WebhookAPI(APIView):
   
   def post(self, request, *args, **kwargs):
        event = None
        print(request.data)
        payload = request.data
        sig_header = request.headers['STRIPE_SIGNATURE']
        
        try:
            event = stripe.Webhook.construct_event(
               payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
           
        except ValueError as e:
           #invalid payload
           print(f"Invalid payload: {e}")
           return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature, handle this error
            print(f"Invalid signature: {e}")
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the event

        if event['type'] == 'checkout.session.completed':
           print('checkout.session.completed')
           session = event['data']['object']
           print(event)

        elif event['type'] == 'checkout.session.expired':
           print('checkout.session.expired')
           session = event['data']['object']
           print(event)

        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))
        return Response({"success":True}, status=status.HTTP_200_OK)