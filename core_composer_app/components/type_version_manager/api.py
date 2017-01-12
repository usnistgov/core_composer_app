"""
Type Version Manager API
"""
from core_composer_app.components.type import api as type_api
from core_composer_app.components.type_version_manager.models import TypeVersionManager
from core_composer_app.components.bucket import api as bucket_api
from core_main_app.components.version_manager import api as version_manager_api


def insert(type_version_manager, type_object, list_bucket_ids=None):
    """Adds a version to a type version manager

    Args:
        type_version_manager:
        type_object:
        list_bucket_ids:

    Returns:

    """
    # save the type in database
    saved_type = type_api.upsert(type_object)
    try:
        # insert the initial template in the version manager
        version_manager_api.insert_version(type_version_manager, saved_type)
        # insert the version manager in database
        version_manager = version_manager_api.upsert(type_version_manager)
        # Add to the selected buckets
        _add_type_to_buckets(version_manager, list_bucket_ids)
        return version_manager
    except Exception, e:
        type_api.delete(saved_type)
        raise e


def get_global_version_managers():
    """Gets all global version managers of a type

    Returns:

    """
    return TypeVersionManager.get_global_version_managers()


def _add_type_to_buckets(version_manager, list_bucket_ids):
    """Add type version manager to buckets

    Args:
        version_manager:
        list_bucket_ids:

    Returns:

    """
    if list_bucket_ids is None:
        return

    # Iterate through list of bucket ids
    for bucket_id in list_bucket_ids:
        # get the bucket using its id
        bucket = bucket_api.get_by_id(bucket_id)
        # add type to bucket
        bucket.types.append(version_manager)
        # update bucket
        bucket_api.upsert(bucket)


def update_type_buckets(version_manager, list_bucket_ids):
    """Removes type from current buckets and puts them in new list

    Args:
        version_manager:
        list_bucket_ids:

    Returns:

    """
    # remove types from current buckets
    _remove_type_from_buckets(version_manager)
    # add types to new list of buckets
    _add_type_to_buckets(version_manager, list_bucket_ids)


def _remove_type_from_buckets(version_manager):
    """Remove the type from all the buckets

    Args:
        version_manager:

    Returns:

    """
    buckets = bucket_api.get_all()

    # Iterate through all buckets
    for bucket in buckets:
        # if type in bucket
        if version_manager in bucket.types:
            # remove type from the bucket
            bucket.types.remove(version_manager)
            # update bucket
            bucket_api.upsert(bucket)
