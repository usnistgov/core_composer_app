"""
Type API
"""
from core_main_app.access_control.api import is_superuser
from core_main_app.access_control.decorators import access_control
from core_main_app.components.template import api as template_api
from core_main_app.components.template.access_control import (
    can_write,
    can_read_id,
)

from core_composer_app.components.type.models import Type
from core_composer_app.utils.xml import check_type_core_support, COMPLEX_TYPE


@access_control(can_write)
def upsert(type_object, request):
    """Save or update the type.

    Args:
        type_object:
        request:

    Returns:

    """
    # Check that the type is supported by the core
    type_definition = check_type_core_support(type_object.content)
    type_object.is_complex = type_definition == COMPLEX_TYPE
    # Save type
    return template_api.upsert(type_object, request=request)


@access_control(can_read_id)
def get(type_id, request):
    """Get a type.

    Args:
        type_id:
        request:

    Returns:

    """
    return Type.get_by_id(type_id)


@access_control(is_superuser)
def get_all(request):
    """List all types.

    Returns:

    """
    return Type.get_all()


@access_control(is_superuser)
def get_all_complex_type(request):
    """List all complex types.

    Returns:

    """
    return Type.get_all_complex_type()


@access_control(can_write)
def delete(type_object, request):
    """Delete the type.

    Returns:

    """
    type_object.delete()
