"""
Type Version Manager model
"""
from core_main_app.components.template_version_manager.models import TemplateVersionManager


class TypeVersionManager(TemplateVersionManager):
    """Manage versions of types.
    """

    @staticmethod
    def get_global_version_managers(_cls=True):
        """Return all Type Version Managers with user set to None.

        Returns:

        """
        return [vm for vm in TypeVersionManager.objects().all() if vm.user is None]

    @staticmethod
    def get_version_managers_by_user(user_id):
        """Return Type Version Managers with user set to user_id.

        Args:
            user_id:

        Returns:

        """
        return [vm for vm in TypeVersionManager.objects().all() if vm.user == str(user_id)]
