from django.db import models
from helper import BaseModel
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

    class Meta:
        db_table = 'orders'
    

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
