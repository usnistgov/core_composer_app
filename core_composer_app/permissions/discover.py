""" Initialize permissions for core composer app.
"""
import logging

from django.contrib.auth.models import Permission, Group

from core_main_app.permissions import rights as main_rights
from core_composer_app.permissions import rights as composer_rights


logger = logging.getLogger(__name__)


def init_permissions():
    """Initialization of groups and permissions."""
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(
            name=main_rights.DEFAULT_GROUP
        )

        # Get composer permissions
        composer_access_perm = Permission.objects.get(
            codename=composer_rights.COMPOSER_ACCESS
        )
        composer_save_template_perm = Permission.objects.get(
            codename=composer_rights.COMPOSER_SAVE_TEMPLATE
        )
        composer_save_type_perm = Permission.objects.get(
            codename=composer_rights.COMPOSER_SAVE_TYPE
        )

        # Add permissions to default group
        default_group.permissions.add(
            composer_access_perm,
            composer_save_template_perm,
            composer_save_type_perm,
        )
    except Exception as exception:
        logger.error(
            "Impossible to init composer permissions: %s", str(exception)
        )
