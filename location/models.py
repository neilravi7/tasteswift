from collections.abc import Iterable
from django.db import models
from django.conf import settings
from helper.models import BaseModel
import geocoder

# Create your models here.

class Address(BaseModel, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  
        null=True,
        blank=True
    )   
    address = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long= models.FloatField(blank=True, null=True)
    
    class Meta:
        db_table = "addresses"

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=settings.MAPBOX_KEY) # will add token here
        self.lat = g.lat
        self.long = g.lng
        return super(Address, self).save(*args, **kwargs)