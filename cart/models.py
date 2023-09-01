from django.db import models
from helper.models import BaseModel
from menu.models import FoodItem
from django.conf import settings


# Create your models here.
class Cart(BaseModel, models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f"{self.customer.email.capitalize()}_CART's"

class CartItem(BaseModel, models.Model):
    cart = models.ForeignKey(
        Cart,
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
        db_table = 'cart_items'