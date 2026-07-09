#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

This is the entry point for all Django management commands such as
runserver, migrate, createsuperuser, etc.
"""
import os
import sys


def main():
    """Run administrative tasks.

    Sets the default Django settings module and executes the command
    line arguments passed to this script.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
