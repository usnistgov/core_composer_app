""" Apps file for setting core package when app is ready
"""
import sys

from django.apps import AppConfig


class ComposerAppConfig(AppConfig):
    """Core composer application settings"""

    name = "core_composer_app"
    verbose_name = "Core Composer App"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            from core_composer_app.permissions import discover

            discover.init_permissions()
