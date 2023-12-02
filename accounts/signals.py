
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.contrib.auth import get_user_model
from vendor.models import Vendor
from customers.models import Customer
from helper.emails import send_account_activation_email

User = get_user_model()

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    print("signal is called")
    try:
        if created:
            if instance.is_customer:
                print("user is customer")
                Customer.objects.create(user=instance)
            elif instance.is_vendor:
                print("user is vendor")
                Vendor.objects.create(user=instance)
            else:
                print("User is admin")

            '''Sending Email code goes here'''
            email_token = str(uuid.uuid4())
            email = instance.email
            send_account_activation_email(email , email_token)          

    except Exception as e:
        print(e)