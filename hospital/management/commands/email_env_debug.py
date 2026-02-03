import os
import importlib

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Print email env/settings lengths without exposing secrets."

    def handle(self, *args, **options):
        env_len = len(os.environ.get("EMAIL_HOST_PASSWORD", ""))
        settings_len = len(settings.EMAIL_HOST_PASSWORD or "")
        settings_module = ""
        settings_file = ""
        module_len = 0
        try:
            settings_module = os.environ["DJANGO_SETTINGS_MODULE"]
            mod = importlib.import_module(settings_module)
            settings_file = getattr(mod, "__file__", "")
            module_len = len(getattr(mod, "EMAIL_HOST_PASSWORD", "") or "")
        except Exception:
            settings_file = ""
        self.stdout.write(f"EMAIL_HOST_PASSWORD env length: {env_len}")
        self.stdout.write(f"EMAIL_HOST_PASSWORD settings length: {settings_len}")
        self.stdout.write(f"EMAIL_HOST_PASSWORD module length: {module_len}")
        self.stdout.write(f"DJANGO_SETTINGS_MODULE: {settings_module}")
        self.stdout.write(f"SETTINGS __file__: {settings_file}")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
