"""
Type Version Manager API
"""
from core_main_app.access_control.api import is_superuser
from core_main_app.access_control.decorators import access_control
from core_main_app.components.template.access_control import can_read
from core_main_app.components.template.access_control import can_read_global
from core_main_app.components.template_version_manager.access_control import can_write
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.utils import get_latest_version_name
import core_main_app.commons.exceptions as exceptions
from core_composer_app.components.bucket import api as bucket_api
from core_composer_app.components.type import api as type_api
from core_composer_app.components.type_version_manager.models import TypeVersionManager


@access_control(can_read)
def get_by_id(version_manager_id, request):
    """Get a type version manager by its id.

    Args:
        version_manager_id:
        request:

    Returns:

    """
    return TypeVersionManager.get_by_id(version_manager_id)


@access_control(can_write)
def insert(type_version_manager, type_object, request, list_bucket_ids=None):
    """Add a version to a type version manager.

    Args:
        type_version_manager:
        type_object:
        request:
        list_bucket_ids:

    Returns:

    """
    # save the type in database
    type_api.upsert(type_object, request=request)
    try:
        # create version manager
        version_manager_api.upsert(type_version_manager, request=request)
        # set version manager
        type_object.version_manager = type_version_manager
        # insert the initial template in the version manager
        if len(type_version_manager.versions) == 0:
            type_object.is_current = True
        # Add to the selected buckets
        bucket_api.add_type_to_buckets(type_version_manager, list_bucket_ids)
        # update display name
        type_object.display_name = get_latest_version_name(type_version_manager)
        # save type
        type_object.save()
        # return version manager
        return type_version_manager
    except Exception as exception:
        type_object.delete()
        raise exception


@access_control(can_read_global)
def get_global_version_managers(request):
    """Get all global version managers of a type.

    Args:
        request:

    Returns:

    """
    return TypeVersionManager.get_global_version_managers()


@access_control(can_read_global)
def get_active_global_version_manager(request):
    """Return all active Version Managers with user set to None.

    Args:
        request:

    Returns:

    """
    return TypeVersionManager.get_active_global_version_manager()


def get_version_managers_by_user(request):
    """Get all global version managers of a user.

    Returns:

    """
    return TypeVersionManager.get_version_managers_by_user(str(request.user.id))


def get_active_version_manager_by_user_id(request):
    """Return all active Version Managers with given user id.

    Returns:

    """
    return TypeVersionManager.get_active_version_manager_by_user_id(
        str(request.user.id)
    )


@access_control(can_read_global)
def get_no_buckets_types(request):
    """Get list of available types not inside a bucket.

    Returns:

    """
    # build list of types
    bucket_types = []
    for bucket in bucket_api.get_all():
        bucket_types += bucket.types.all()

    all_types = get_global_version_managers(request=request)
    no_bucket_types = [
        type_version_manager
        for type_version_manager in all_types
        if type_version_manager not in bucket_types
    ]
    return no_bucket_types


@access_control(is_superuser)
def get_all_version_manager(request):
    """Return all Type Version Managers of all users.

    Returns:

    """
    return TypeVersionManager.get_all_type_version_manager()
