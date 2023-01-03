from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from store_app.models import Customer

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()