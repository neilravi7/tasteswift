from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as gl
from helper.models import BaseModel
from cart.models import Cart, CartItem
from location.models import Address

# Create your models here.
class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User Require Email Field')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)



class User(BaseModel, AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(gl('email address'), unique=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return self.email
    
    def __unicode__(self):
        return self.id
    
    def get_cart(self):
        cart, created = Cart.objects.get_or_create(customer=self)
        return cart
    
    def get_cart_item(self):
        cart = self.get_cart()
        cart_items = CartItem.objects.filter(cart=cart)
        return cart_items
    
    def get_user_phone(self):
        if self.is_customer:
            phone = self.user_as_customer.phone
            return phone
        if self.is_vendor:
            phone = self.user_as_vendor.phone
            return phone
    
    def get_user_address(self):
        address = Address.objects.filter(user_id=self.id).first()
        if address:
            return address.address
        else:
            return ""

        