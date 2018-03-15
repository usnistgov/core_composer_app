"""REST views for the type version manager API
"""
from django.utils.decorators import method_decorator

from core_composer_app.components.type_version_manager import api as type_version_manager_api
from core_composer_app.rest.type_version_manager.abstract_views import AbstractTypeList
from core_main_app.rest.template_version_manager.views import AbstractTemplateVersionManagerList
from core_main_app.utils.decorators import api_staff_member_required


class GlobalTypeVersionManagerList(AbstractTemplateVersionManagerList):
    """ List all global type version managers.
    """

    def get_template_version_managers(self):
        """ Get global ty[e version managers

        Returns:

        """
        return type_version_manager_api.get_global_version_managers()


class UserTypeVersionManagerList(AbstractTemplateVersionManagerList):
    """ List all user type version managers.
    """

    def get_template_version_managers(self):
        """ Get all user type version managers.

        Returns:

        """
        return type_version_manager_api.get_version_managers_by_user(user_id=self.request.user.id)


class UserTypeList(AbstractTypeList):
    """ Create a user type.
    """
    def post(self, request):
        """ Create a user type.

        Args:
            request:

        Returns:

        """
        return super(UserTypeList, self).post(request)

    def get_user(self):
        return str(self.request.user.id)


class GlobalTypeList(AbstractTypeList):
    """ Create a global type.
    """
    @method_decorator(api_staff_member_required())
    def post(self, request):
        """ Create a global type.

        Args:
            request:

        Returns:

        """
        return super(GlobalTypeList, self).post(request)

    def get_user(self):
        return None
