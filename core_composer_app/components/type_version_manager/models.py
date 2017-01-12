"""
Type Version Manager model
"""
from core_main_app.components.template_version_manager.models import TemplateVersionManager


class TypeVersionManager(TemplateVersionManager):
    """Manages versions of types"""

    @staticmethod
    def get_global_version_managers():
        """Returns all Type Version Managers with user set to None

        Returns:

        """
        return [vm for vm in TypeVersionManager.objects.all() if vm.user is None]
