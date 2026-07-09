"""
Posts application configuration.

This module configures the posts Django application for managing
social media posts, comments, and likes.
"""

from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Configuration class for the posts application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
