"""
Type Version Manager model
"""
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.version_manager.models import VersionManager


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

    @staticmethod
    def get_all_type_version_manager_except_user_id(user_id):
        """ Return all Version Managers of all users except user with given user id.

        Args:
            user_id:

        Returns:

        """
        # FIXME: construct the cls with super in VersionManager TemplateVersionManager TypeVersionManager
        cls = ".".join((VersionManager.__name__, TemplateVersionManager.__name__, TypeVersionManager.__name__))
        return VersionManager.objects(_cls=cls, user__nin=str(user_id)).all()
