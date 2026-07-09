"""
Signal handlers for the accounts application.

Automatically creates and saves a Profile instance whenever a new User
is created, ensuring every user has an associated profile.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile automatically when a new User is created.

    Args:
        sender: The model class that sent the signal (User).
        instance: The actual User instance that was saved.
        created: Boolean indicating if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the associated Profile whenever the User instance is saved.

    This ensures that any changes to the User model are propagated
    to the linked Profile.

    Args:
        sender: The model class that sent the signal (User).
        instance: The actual User instance that was saved.
        **kwargs: Additional keyword arguments.
    """
    instance.profile.save()
