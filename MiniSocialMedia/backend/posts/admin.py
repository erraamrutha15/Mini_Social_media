"""
Admin configuration for the posts application.

Registers the Post, Comment, and Like models with the Django admin
interface for easy content management through the admin panel.
"""

from django.contrib import admin

from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model."""

    list_display = ('author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model."""

    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin configuration for the Like model."""

    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
