"""Serializers used throughout the Rest API
"""
from core_composer_app.components.type_version_manager.models import TypeVersionManager
from core_composer_app.components.type.models import Type
from core_main_app.commons.serializers import BasicSerializer
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.serializers import CharField


class TypeSerializer(DocumentSerializer):
    """
        Type serializer
    """
    class Meta:
        model = Type
        fields = "__all__"


class TypeVersionManagerSerializer(DocumentSerializer):
    """
        Type Version Manager serializer
    """
    class Meta:
        model = TypeVersionManager
        fields = "__all__"


class CreateTypeSerializer(BasicSerializer):
    """
        Type serializer (creation)
    """
    filename = CharField(required=True)
    content = CharField(required=True)

    def create(self, validated_data):
        """Creates a Type object

        Args:
            validated_data:

        Returns:

        """
        return Type(**validated_data)


class CreateTypeVersionManagerSerializer(BasicSerializer):
    """
        Type Version Manager serializer (creation)
    """
    title = CharField(required=True)

    def create(self, validated_data):
        """Creates a Type Version Manager

        Args:
            validated_data:

        Returns:

        """
        return TypeVersionManager(**validated_data)
