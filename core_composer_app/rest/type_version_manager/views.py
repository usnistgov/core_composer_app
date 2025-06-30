""" REST views for the type version manager API
"""

from django.db.migrations.serializer import TypeSerializer
from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from rest_framework.permissions import IsAuthenticated

from core_composer_app.components.type_version_manager import (
    api as type_version_manager_api,
)
from core_composer_app.rest.type_version_manager.abstract_views import (
    AbstractTypeList,
)
from core_composer_app.rest.type_version_manager.serializers import (
    TypeVersionManagerSerializer,
    CreateTypeSerializer,
)
from core_main_app.rest.template_version_manager.views import (
    AbstractTemplateVersionManagerList,
)
from core_main_app.utils.decorators import api_staff_member_required


@extend_schema(
    tags=["Type Version Manager"],
    description="List all global type version managers",
)
class GlobalTypeVersionManagerList(AbstractTemplateVersionManagerList):
    """List all global type version managers"""

    @extend_schema(
        summary="Get global type version managers",
        description="Retrieve a list of all global type version managers",
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by title",
            ),
            OpenApiParameter(
                name="is_disabled",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter by is_disabled",
            ),
        ],
        responses={
            200: TypeVersionManagerSerializer(many=True),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        return super().get(request)

    def get_template_version_managers(self):
        """Get global type version managers
        Returns:
            TypeVersionManager
        """
        return type_version_manager_api.get_global_version_managers(
            request=self.request
        )


@extend_schema(
    tags=["Type Version Manager"],
    description="List all user type version managers",
)
class UserTypeVersionManagerList(AbstractTemplateVersionManagerList):
    """List all user type version managers"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Get user type version managers",
        description="Retrieve a list of all type version managers for the current user",
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by title",
            ),
            OpenApiParameter(
                name="is_disabled",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter by is_disabled",
            ),
        ],
        responses={
            200: TypeVersionManagerSerializer(many=True),
            403: OpenApiResponse(description="Access Forbidden"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        return super().get(request)

    def get_template_version_managers(self):
        """Get all user type version managers
        Returns:
            TypeVersionManager
        """
        return type_version_manager_api.get_version_managers_by_user(
            request=self.request
        )


@extend_schema(
    tags=["Type"],
    description="Create a user type",
)
class UserTypeList(AbstractTypeList):
    """Create a user type"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Create a user type & type version manager",
        description="Create a new user type and its associated type version manager",
        request=CreateTypeSerializer,
        responses={
            201: TypeSerializer,
            400: OpenApiResponse(description="Validation Error / Bad Request"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Create a user type",
                summary="Create a new user type",
                description="Create a new user type and its associated type version manager",
                request_only=True,
                value={
                    "title": "title",
                    "filename": "filename",
                    "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:simpleType name='root'/></xs:schema>",
                },
            ),
        ],
    )
    def post(self, request):
        """Create a user type & type version manager
        Parameters:
            {
              "title": "title",
              "filename": "filename",
              "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'> <xs:simpleType name='root'/></xs:schema>"
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
        return super().post(request)

    def get_user(self):
        """Retrieve user from the request"""
        return str(self.request.user.id)


@extend_schema(
    tags=["Type"],
    description="Create a global type",
)
class GlobalTypeList(AbstractTypeList):
    """Create a global type"""

    @extend_schema(
        summary="Create a global type & type version manager",
        description="Create a new global type and its associated type version manager",
        request=CreateTypeSerializer,
        responses={
            201: TypeSerializer,
            400: OpenApiResponse(description="Validation Error / Bad Request"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Create a global type",
                summary="Create a new global type",
                description="Create a new global type and its associated type version manager",
                request_only=True,
                value={
                    "title": "title",
                    "filename": "filename",
                    "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:simpleType name='root'/></xs:schema>",
                },
            ),
        ],
    )
    @method_decorator(api_staff_member_required())
    def post(self, request):
        """Create a global type & type version manager
        Parameters:
            {
              "title": "title",
              "filename": "filename",
              "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'> <xs:simpleType name='root'/></xs:schema>"
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
        return super().post(request)

    def get_user(self):
        """None for global type"""
        return None
