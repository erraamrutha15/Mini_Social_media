"""
Admin configuration for the accounts application.

Registers the Profile and Follow models with the Django admin interface
for easy management through the admin panel.
"""

from django.contrib import admin

from .models import Profile, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""

    list_display = ('user', 'bio', 'created_at')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin configuration for the Follow model."""

    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)
