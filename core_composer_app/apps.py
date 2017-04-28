""" Apps file for setting core package when app is ready
"""
from django.apps import AppConfig
import core_composer_app.permissions.discover as discover


class ComposerAppConfig(AppConfig):
    """ Core composer application settings
    """
    name = 'core_composer_app'

    def ready(self):
        """ Runs when the app is ready

        Returns:

        """
        discover.init_permissions()
