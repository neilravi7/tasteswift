from django.db import models
from helper.models import BaseModel
from django.conf import settings
from menu.models import FoodItem

# Create your models here.

class Order(BaseModel, models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('delivered', 'Delivered'),
    )

    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='order_as_vendor'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='order_as_customer'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    display_id = models.CharField(max_length=10)
    stripe_checkout_id = models.CharField(max_length=80, null=True, blank=True)
    payment_status=models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        db_table = 'orders'

    def get_order_items(self):
        return OrderItem.objects.filter(order_id=self.id)
    
    def get_serialize_items(self):
        items = self.get_order_items()
        if len(items) == 0:
            return []
        else:
            return [
            {
                "id":item.id, 
                "name":item.food_item.name, 
                "image_url":item.food_item.image_url,
                "quantity":item.quantity
            } 
                for item in items
            ]
    

class OrderItem(BaseModel, models.Model):
    order = models.ForeignKey(
        Order,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    food_item = models.ForeignKey(
        FoodItem,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_items'