from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from helper.models import BaseModel

# Create your models here.
class Category(BaseModel, models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(max_length=250, blank=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name.capitalize()
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        self.image_url = "https://delishnow.s3.us-east-005.backblazeb2.com/hero-1.jpg"
        return super(Category, self).save(*args, **kwargs)


class FoodItem(BaseModel, models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'food_item'

    def __str__(self):
        return self.name.capitalize()
    
    def clean(self):
        self.name = self.name.capitalize()
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        self.image_url = "https://delishnow.s3.us-east-005.backblazeb2.com/hero-1.jpg"
        return super(FoodItem, self).save(*args, **kwargs)
