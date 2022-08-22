"""Serializers used throughout the bucket Rest API
"""
from django.http import Http404
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from core_main_app.commons.exceptions import DoesNotExist
from core_composer_app.components.bucket import api as bucket_api
from core_composer_app.components.bucket.models import Bucket


class BucketSerializer(ModelSerializer):
    """Bucket serializer"""

    class Meta:
        """Meta"""

        model = Bucket
        fields = "__all__"
        read_only_fields = (
            "id",
            "color",
        )

    def create(self, validated_data):
        """
        Create and return a new `Bucket` instance, given the validated data.
        """
        # Create data
        bucket = Bucket(label=validated_data["label"])
        # Save the data
        bucket_api.upsert(bucket)
        bucket.types.set(validated_data.get("types", []))
        return bucket

    def update(self, instance, validated_data):
        """
        Update and return an existing `Bucket` instance, given the validated data.
        """
        instance.label = validated_data.get("label", instance.label)
        bucket_api.upsert(instance)
        return instance


class BucketsSerializer(ModelSerializer):
    """Buckets serializer."""

    id = CharField()

    class Meta:
        """Meta"""

        model = Bucket
        fields = ("id",)

    def validate_id(self, id):
        """Validate id field

        Args:
            id:

        Returns:

        """
        try:
            bucket_api.get_by_id(id)
            return id
        except DoesNotExist:
            raise Http404
