""" Initialize permissions for core composer app.
"""
import logging

from django.contrib.auth.models import Permission, Group

from core_composer_app.permissions import rights as composer_rights
from core_main_app.permissions import rights as main_rights

logger = logging.getLogger(__name__)


def init_permissions():
    """Initialization of groups and permissions."""
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(
            name=main_rights.default_group
        )

        # Get composer permissions
        composer_access_perm = Permission.objects.get(
            codename=composer_rights.composer_access
        )
        composer_save_template_perm = Permission.objects.get(
            codename=composer_rights.composer_save_template
        )
        composer_save_type_perm = Permission.objects.get(
            codename=composer_rights.composer_save_type
        )

        # Add permissions to default group
        default_group.permissions.add(
            composer_access_perm, composer_save_template_perm, composer_save_type_perm
        )
    except Exception as e:
        logger.error("Impossible to init composer permissions: %s" % str(e))
