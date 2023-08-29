from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, OpeningHours, Day


@receiver(post_save, sender=Vendor)
def post_save_user(sender, instance, created, **kwargs):
    try:
        if created:
            for day_choice in Day.choices:
                day, day_display = day_choice
                OpeningHours.objects.create(
                    restaurant=instance,
                    day=day,
                    opening_time='09:00:00',
                    closing_time='20:00:00'
                )
            print("Created Days timings")    
    except Exception as e:
        print(e)