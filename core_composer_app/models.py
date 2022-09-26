"""Composer models
"""
from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from core_composer_app.permissions import rights


class Composer(models.Model):
    """Composer object"""

    class Meta:
        """Meta"""

        verbose_name = "core_composer_app"
        default_permissions = ()
        permissions = (
            (
                rights.COMPOSER_ACCESS,
                get_formatted_name(rights.COMPOSER_ACCESS),
            ),
            (
                rights.COMPOSER_SAVE_TEMPLATE,
                get_formatted_name(rights.COMPOSER_SAVE_TEMPLATE),
            ),
            (
                rights.COMPOSER_SAVE_TYPE,
                get_formatted_name(rights.COMPOSER_SAVE_TYPE),
            ),
        )
