# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserInfo

# Signal to create UserInfo when a new User is created
@receiver(post_save, sender=User)
def create_userinfo(sender, instance, created, **kwargs):
    if created:  # This only runs when a new User is created
        UserInfo.objects.get_or_create(user=instance)  # Safely create UserInfo if it doesn't exist

# Signal to save UserInfo when the User is saved (to keep them in sync)
@receiver(post_save, sender=User)
def save_userinfo(sender, instance, **kwargs):
    if hasattr(instance, 'userinfo'):
        instance.userinfo.save()