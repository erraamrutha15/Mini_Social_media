"""
Accounts application configuration.

This module configures the accounts Django application and ensures
that signal handlers are loaded when the application starts.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration class for the accounts application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """Import signal handlers when the application is ready.

        This ensures that the post_save signal for automatic Profile
        creation is connected when Django starts up.
        """
        import accounts.signals  # noqa: F401
