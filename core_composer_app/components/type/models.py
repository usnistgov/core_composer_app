"""
Type models
"""

from core_main_app.components.template.models import Template
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


class Type(Template):
    """Type class
    """

    @staticmethod
    def get_by_id(type_id):
        """Returns a type given its id

        Args:
            type_id:

        Returns:

        """
        try:
            return Type.objects().get(pk=str(type_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_all():
        """Returns all types

        Returns:

        """
        return Type.objects().all()
