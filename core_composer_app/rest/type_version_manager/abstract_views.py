""" REST abstract views for the type version manager API
"""

from abc import ABCMeta, abstractmethod

from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from core_main_app.commons.exceptions import NotUniqueError, XSDError
from core_main_app.rest.template_version_manager.abstract_views import (
    AbstractTemplateVersionManagerDetail,
)
from core_main_app.utils.decorators import api_staff_member_required
from core_composer_app.rest.type_version_manager.serializers import (
    CreateTypeSerializer,
    TypeVersionManagerSerializer,
)


class AbstractTypeList(
    APIView,
    metaclass=ABCMeta,
):
    """Create a type & type version manager"""

    def post(self, request):
        """Create a type & type version manager

        Parameters:

            {
                "title": "title",
                "filename": "filename",
                "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:simpleType name='root'/></xs:schema>"
            }

        Note:

            "dependencies_dict": json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Type
            - code: 400
              content: Validation error / bad request
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializers
            type_serializer = CreateTypeSerializer(
                data=request.data, context={"request": request}
            )
            type_version_manager_serializer = TypeVersionManagerSerializer(
                data=request.data
            )

            # Validate data
            type_serializer.is_valid(raise_exception=True)
            type_version_manager_serializer.is_valid(raise_exception=True)

            # Save data
            type_version_manager_object = type_version_manager_serializer.save(
                user=self.get_user()
            )
            type_serializer.save(
                type_version_manager=type_version_manager_object,
                user=self.get_user(),
            )

            return Response(
                type_serializer.data, status=status.HTTP_201_CREATED
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except NotUniqueError:
            content = {"message": "A type with the same title already exists."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except XSDError as xsd_error:
            content = {"message": "XSD Error: " + str(xsd_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @abstractmethod
    def get_user(self):
        """Get a user"""
        raise NotImplementedError("get_user method is not implemented.")


class TypeVersion(AbstractTemplateVersionManagerDetail):
    """Create a type version"""

    @method_decorator(api_staff_member_required())
    def post(self, request, pk):
        """Create a type version

        Parameters:

            {
                "filename": "filename",
                "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:simpleType name='root'/></xs:schema>"
            }

        Note:

            "dependencies_dict": json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Type
            - code: 400
              content: Validation error / bad request
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            type_version_manager_object = self.get_object(pk)

            # Build serializers
            type_serializer = CreateTypeSerializer(
                data=request.data, context={"request": request}
            )

            # Validate data
            type_serializer.is_valid(raise_exception=True)

            # Save data
            type_serializer.save(
                type_version_manager=type_version_manager_object,
                user=type_version_manager_object.user,
            )

            return Response(
                type_serializer.data, status=status.HTTP_201_CREATED
            )
        except Http404:
            content = {"message": "Type Version Manager not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
