#!/usr/bin/env python
"""
manage.py - Django's command-line utility for administrative tasks.

Project: Hospital Management System
Maintainer: Param Purohit
"""

import os
import sys
import logging

def main():
    """Main entry point for Django administrative commands."""
    
    # Default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')

    # Optional: Log environment info (useful in production logs)
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Using settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

    # Environment warning for development
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'hospitalmanagement.settings':
        print("🔧 Running in development mode. Make sure to configure production settings before deployment.")

    try:
        # Import and run the Django management utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "❌ Couldn't import Django. Ensure it's installed and "
            "available on your PYTHONPATH environment variable. "
            "Did you forget to activate a virtual environment?"
        ) from exc

    # Execute command-line tasks
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
