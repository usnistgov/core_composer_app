"""Bucket model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces
from core_composer_app.components.type_version_manager.models import TypeVersionManager


class Bucket(models.Model):
    """Bucket class to store types by domain."""

    label = models.CharField(unique=True, max_length=200)
    color = models.CharField(unique=True, max_length=7, default=None)
    types = models.ManyToManyField(TypeVersionManager, default=[], blank=True)

    @staticmethod
    def get_by_id(bucket_id):
        """Return a bucket given its id.

        Args:
            bucket_id:

        Returns:

        """
        try:
            return Bucket.objects.get(pk=str(bucket_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Return all buckets.

        Returns:

        """
        return Bucket.objects.all()

    @staticmethod
    def get_colors():
        """Return all colors.

        Returns:

        """
        return Bucket.objects.values_list("color", flat=True)

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            self.clean()
            return self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def add_type(self, type_version_manager):
        """Add type to bucket.

        Args:
            type_version_manager:

        Returns:

        """
        self.types.add(type_version_manager)

    def remove_type(self, type_version_manager):
        """Remove type from bucket.

        Args:
            type_version_manager:

        Returns:

        """
        self.types.remove(type_version_manager)

    def __str__(self):
        """Bucket as string

        Returns:

        """
        return self.label

    def clean(self):
        """Clean before saving

        Returns:

        """
        not_empty_or_whitespaces(self.label)
        self.label = self.label.strip()
