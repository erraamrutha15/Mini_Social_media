"""
Models for the accounts application.

Defines the Profile and Follow models that extend Django's built-in User model
to support user profiles with bios and a follower/following relationship system.
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extended user profile model.

    Each User automatically gets a Profile instance (created via signal)
    that stores additional information like a biography.

    Attributes:
        user: One-to-one link to Django's built-in User model.
        bio: Optional biography text, up to 500 characters.
        created_at: Timestamp when the profile was created.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text='The user this profile belongs to.'
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text='A short biography about the user (max 500 characters).'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when this profile was created.'
    )

    def __str__(self):
        """Return a human-readable string representation of the profile."""
        return f"Profile of {self.user.username}"

    class Meta:
        """Meta options for the Profile model."""
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Follow(models.Model):
    """
    Model representing a follow relationship between two users.

    A Follow instance means that `follower` is following `following`.
    The unique_together constraint prevents duplicate follow relationships.

    Attributes:
        follower: The user who is following another user.
        following: The user who is being followed.
        created_at: Timestamp when the follow relationship was created.
    """

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_set',
        help_text='The user who is following.'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers_set',
        help_text='The user who is being followed.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the follow relationship was established.'
    )

    def __str__(self):
        """Return a human-readable string representation of the follow."""
        return f"{self.follower.username} follows {self.following.username}"

    class Meta:
        """Meta options for the Follow model."""
        unique_together = ('follower', 'following')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
