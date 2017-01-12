"""
Type API
"""
from core_composer_app.utils.xml import check_type_core_support
from core_main_app.components.template import api as template_api
from core_composer_app.components.type.models import Type


def upsert(type_object):
    """Saves or Updates the type

    Args:
        type_object:

    Returns:

    """
    check_type_core_support(type_object.content)
    return template_api.upsert(type_object)


def get(type_id):
    """Gets a type

    Args:
        type_id:

    Returns:

    """
    return template_api.get(type_id)


def get_all():
    """Lists all types

    Returns:

    """
    return Type.get_all()


def delete(type_object):
    """Deletes the type

    Returns:

    """
    type_object.delete()
