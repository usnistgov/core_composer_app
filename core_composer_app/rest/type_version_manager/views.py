"""REST views for the type version manager API
"""
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from core_composer_app.components.type_version_manager import api as type_version_manager_api
from core_main_app.components.version_manager import api as version_manager_api
from core_composer_app.rest.serializers import TypeVersionManagerSerializer
from core_main_app.commons import exceptions as exceptions


@api_view(['GET'])
def get_by_id(request):
    """Return a type version manager by its id.

    GET /rest/type-version-manager/get?id=<id>

    Args:
        request:

    Returns:

    """
    try:
        # Get parameters
        type_version_manager_id = request.query_params.get('id', None)

        # Check parameters
        if type_version_manager_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        type_version_manager_object = version_manager_api.get(type_version_manager_id)
        # Serialize object
        type_version_manager_serializer = TypeVersionManagerSerializer(type_version_manager_object)
        # Return response
        return Response(type_version_manager_serializer.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {'message': 'No type version manager could be found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_globals(request):
    """Return http response with all global type version managers.

    GET /rest/type-version-manager/get/all/global

    Args:
        request:

    Returns:

    """
    try:
        type_version_managers = type_version_manager_api.get_global_version_managers()
        type_version_manager_serializer = TypeVersionManagerSerializer(type_version_managers, many=True)
        return Response(type_version_manager_serializer.data, status=status.HTTP_200_OK)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_by_user(request):
    """Return http response with all type version managers of a user.

    GET /rest/type-version-manager/get/all/user

    Args:
        request:

    Returns:

    """
    try:
        type_version_managers = type_version_manager_api.get_version_managers_by_user(user_id=request.user.id)
        template_version_manager_serializer = TypeVersionManagerSerializer(type_version_managers, many=True)
        return Response(template_version_manager_serializer.data, status=status.HTTP_200_OK)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)