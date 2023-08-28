from django.db import models
from django.conf import settings
from helper.models import BaseModel

# Create your models here.

class Vendor(BaseModel, models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='user_as_vendor'
    )
    photo = models.URLField(blank=True, null=True)
    business_name = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Leave location and reviees s for now

    class META:
        db_table = "vendors"

    def __str__(self) -> str:
        return self.full_name.capitalize()
    
    def __unicode__(self):
        return self.id
