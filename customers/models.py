from typing import Iterable, Optional
from django.db import models
from django.conf import settings
from helper.models import BaseModel
# Create your models here.

class Customer(BaseModel, models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='user_as_customer'
    )
    photo = models.URLField(blank=True, null=True)
    full_name = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Leave location and wishlist for now

    class META:
        db_table = "customers"

    def __str__(self) -> str:
        return self.full_name.capitalize()
    

    def save(self, *args, **kwargs):
        self.photo = "http://placebeard.it/640x480"
        return super(Customer, self).save(*args, **kwargs)
    
    
