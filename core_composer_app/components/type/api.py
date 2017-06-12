"""
Type API
"""
from core_composer_app.utils.xml import check_type_core_support
from core_main_app.components.template import api as template_api
from core_composer_app.components.type.models import Type


def upsert(type_object):
    """Save or update the type.

    Args:
        type_object:

    Returns:

    """
    # Check that the type is supported by the core
    check_type_core_support(type_object.content)
    # Save type
    return template_api.upsert(type_object)


def get(type_id):
    """Get a type.

    Args:
        type_id:

    Returns:

    """
    return Type.get_by_id(type_id)


def get_all():
    """List all types.

    Returns:

    """
    return Type.get_all()


def delete(type_object):
    """Delete the type.

    Returns:

    """
    type_object.delete()
