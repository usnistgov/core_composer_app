"""
Type Version Manager model
"""
from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons import exceptions
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)


class TypeVersionManager(TemplateVersionManager):
    """Manage versions of types."""

    _class_name = "VersionManager.TemplateVersionManager.TypeVersionManager"

    @property
    def class_name(self):
        """Class name"""
        return TypeVersionManager._class_name

    @staticmethod
    def get_by_id(version_manager_id):
        """Return Version Managers by id.

        Args:
            version_manager_id:

        Returns:

        """
        try:
            return TypeVersionManager.objects.get(pk=str(version_manager_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_global_version_managers(_cls=True):
        """Return all Type Version Managers with user set to None.

        Returns:

        """
        return TypeVersionManager.objects.filter(user=None).all()

    @staticmethod
    def get_active_global_version_manager(_cls=True):
        """Return all active Type Version Managers with user set to None.

        Returns:

        """
        return TypeVersionManager.objects.filter(
            is_disabled=False, user=None
        ).all()

    @staticmethod
    def get_version_managers_by_user(user_id):
        """Return Type Version Managers with user set to user_id.

        Args:
            user_id:

        Returns:

        """
        return TypeVersionManager.objects.filter(user=str(user_id)).all()

    @staticmethod
    def get_active_version_manager_by_user_id(user_id):
        """Return active Type Version Managers with user set to user_id.

        Args:
            user_id:

        Returns:

        """
        return TypeVersionManager.objects.filter(
            is_disabled=False, user=str(user_id)
        ).all()

    @staticmethod
    def get_all_type_version_manager():
        """Return all Version Managers of all users.

        Args:

        Returns:

        """
        return TypeVersionManager.objects.filter(
            _cls=TypeVersionManager._class_name
        ).all()
