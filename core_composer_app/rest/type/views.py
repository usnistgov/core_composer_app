"""REST views for the template API
"""
from rest_framework.exceptions import ValidationError

from core_main_app.rest.template.views import _load_dependencies
from rest_framework.decorators import api_view

from core_composer_app.rest.serializers import TypeSerializer, CreateTypeSerializer, CreateTypeVersionManagerSerializer
from core_main_app.commons import exceptions as exceptions
from core_composer_app.components.type import api as type_api
from core_composer_app.components.type_version_manager import api as type_version_manager_api
from rest_framework.response import Response
from rest_framework import status

from core_main_app.components.template.api import init_template_with_dependencies


@api_view(['GET'])
def get_by_id(request):
    """GET /rest/type?id=<id>

    Args:
        request:

    Returns:

    """
    try:
        # Get parameters
        type_id = request.query_params.get('id', None)

        # Check parameters
        if type_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        type_object = type_api.get(type_id)

        # Serialize object
        type_serializer = TypeSerializer(type_object)
        # Return response
        return Response(type_serializer.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {'message': 'No type could be found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _post(request):
    """ POST /rest/type
    {
    "filename": "filename",
    "title": "title",
    "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:simpleType name='root'/></xs:schema>"
    }

    Note: "dependencies"= json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

    Args:
        request:

    Returns:

    """
    try:
        # Build serializers
        create_type_serializer = CreateTypeSerializer(data=request.data)
        create_type_version_manager_serializer = CreateTypeVersionManagerSerializer(data=request.data)

        # Validate data
        create_type_serializer.is_valid(True)
        create_type_version_manager_serializer.is_valid(True)

        # Deserialize object
        type_object = create_type_serializer.create(create_type_serializer.data)
        type_version_manager_object = create_type_version_manager_serializer.create(
            create_type_version_manager_serializer.data)

        # Get type parameters
        dependencies = request.data.get('dependencies', None)

        # If dependencies, load the dict from json
        dependencies_dict = _load_dependencies(dependencies)

        # Update the content of the type with dependencies
        init_template_with_dependencies(type_object, dependencies_dict)

        # Create the type and its type version manager
        type_version_manager_api.insert(type_version_manager_object, type_object)

        # Returns the serialized type
        type_serializer = TypeSerializer(type_object)
        return Response(type_serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as validation_exception:
        content = {'message': validation_exception.detail}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def type(request):
    """Type api

    Args:
        request:

    Returns:

    """
    if request.method == 'POST':
        return _post(request)
