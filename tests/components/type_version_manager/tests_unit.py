"""Type Version Manager test cases
"""
from unittest.case import TestCase
from unittest.mock import Mock, patch, MagicMock

from django.core import exceptions as django_exceptions
from django.db import IntegrityError
from django.test import override_settings

from core_composer_app.components.bucket.models import Bucket
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager import (
    api as version_manager_api,
)
from core_composer_app.components.type_version_manager.api import (
    get_no_buckets_types,
)
from core_composer_app.components.type_version_manager.models import (
    TypeVersionManager,
)
from core_main_app.commons.exceptions import CoreError, ModelError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestTypeVersionManagerInsert(TestCase):
    """Test Type Version Manager Insert"""

    @patch.object(TypeVersionManager, "save")
    @patch.object(Type, "save")
    def test_create_version_manager_raises_exception_if_type_not_supported(
        self, mock_save_type, mock_save_type_version_manager
    ):
        """test_create_version_manager_raises_exception_if_type_not_supported"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        type_filename = "schema.xsd"
        type_content = (
            "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        )
        type_object = _create_type(type_filename, type_content)

        mock_save_type.return_value = type_object

        version_manager = _create_type_version_manager(title="Schema")
        mock_save_type_version_manager.return_value = version_manager

        # Act + Assert
        with self.assertRaises(CoreError):
            version_manager_api.insert(
                version_manager, type_object, request=mock_request
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_create_version_manager_returns_version_manager(
        self,
    ):
        """test_create_version_manager_returns_version_manager"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type = MagicMock()
        mock_type.filename = "schema.xsd"
        mock_type.content = (
            "<schema xmlns='http://www.w3.org/2001/XMLSchema'><simpleType name='type'>"
            "<restriction base='string'><enumeration value='test'/></restriction>"
            "</simpleType></schema>"
        )
        mock_version_manager = MagicMock()

        # Act
        result = version_manager_api.insert(
            mock_version_manager, mock_type, request=mock_request
        )

        # Assert
        self.assertEqual(result, mock_version_manager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(Type, "dependencies")
    @patch.object(Type, "delete")
    @patch.object(Type, "save_template")
    @patch.object(TypeVersionManager, "save_version_manager")
    def test_insert_manager_raises_api_error_if_title_already_exists(
        self,
        mock_version_manager_save,
        mock_save,
        mock_delete,
        mock_dependencies,
    ):
        """test_insert_manager_raises_api_error_if_title_already_exists"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        type_filename = "schema.xsd"
        type_object = _create_type(type_filename)

        mock_save.return_value = type_object
        mock_delete.return_value = None
        mock_version_manager = _create_type_version_manager(title="Schema")
        mock_version_manager_save.side_effect = IntegrityError("")

        mock_dependencies.return_value = MockDependencies()

        # Act + Assert
        with self.assertRaises(IntegrityError):
            version_manager_api.insert(
                mock_version_manager, type_object, request=mock_request
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(Type, "save")
    def test_create_version_manager_raises_exception_if_error_in_create_type(
        self, mock_save
    ):
        """test_create_version_manager_raises_exception_if_error_in_create_type"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        type_filename = "schema.xsd"
        type_object = _create_type(type_filename)

        mock_version_manager = _create_mock_type_version_manager(
            title="Schema"
        )
        mock_save.side_effect = ModelError("")

        # Act + Assert
        with self.assertRaises(ModelError):
            version_manager_api.insert(
                mock_version_manager, type_object, request=mock_request
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(Type, "dependencies")
    @patch.object(Type, "delete")
    @patch.object(TypeVersionManager, "save_version_manager")
    @patch.object(Type, "save_template")
    def test_create_version_manager_raises_exception_if_error_in_create_version_manager(
        self,
        mock_save,
        mock_save_version_manager,
        mock_delete,
        mock_dependencies,
    ):
        """test_create_version_manager_raises_exception_if_error_in_create_version_manager"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        type_filename = "Schema.xsd"
        type_object = _create_type(type_filename)

        mock_save.return_value = type_object
        version_manager = _create_type_version_manager(title="Schema")
        mock_save_version_manager.side_effect = (
            django_exceptions.ValidationError("")
        )
        mock_delete.return_value = None

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(
                version_manager, type_object, request=mock_request
            )


class TestTypeVersionManagerGetGlobalVersions(TestCase):
    """Test Type Version Manager Get Global Versions"""

    @patch.object(TypeVersionManager, "get_global_version_managers")
    def test_get_global_version_managers_returns_types(
        self, mock_get_global_version_managers
    ):
        """test_get_global_version_managers_returns_types"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type1 = _create_mock_type()
        mock_type2 = _create_mock_type()

        mock_get_global_version_managers.return_value = [
            mock_type1,
            mock_type2,
        ]

        result = version_manager_api.get_global_version_managers(
            request=mock_request
        )

        # Assert
        self.assertTrue(all(isinstance(item, Type) for item in result))


class TestTypeVersionManagerGetActiveGlobalVersions(TestCase):
    """Test Type Version Manager Get Active Global Versions"""

    @patch.object(TypeVersionManager, "get_active_global_version_manager")
    def test_get_active_global_version_managers_returns_types(
        self, mock_get_active_global_version_manager
    ):
        """test_get_active_global_version_managers_returns_types"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type1 = _create_mock_type()
        mock_type2 = _create_mock_type()

        mock_get_active_global_version_manager.return_value = [
            mock_type1,
            mock_type2,
        ]

        result = version_manager_api.get_active_global_version_manager(
            request=mock_request
        )

        # Assert
        self.assertTrue(all(isinstance(item, Type) for item in result))


class TestTypeVersionManagerGetVersionManagersByUser(TestCase):
    """Test Type Version Manager Get Version Manager By User"""

    @patch.object(TypeVersionManager, "get_version_managers_by_user")
    def test_get_version_managers_by_user_returns_types_with_given_user_id(
        self, mock_get_version_managers_by_user
    ):
        """test_get_version_managers_by_user_returns_types_with_given_user_id"""

        # Arrange
        user_id = "10"
        mock_user = create_mock_user(user_id=user_id, is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type1 = _create_mock_type_version_manager(user=user_id)
        mock_type2 = _create_mock_type_version_manager(user=user_id)

        mock_get_version_managers_by_user.return_value = [
            mock_type1,
            mock_type2,
        ]

        result = version_manager_api.get_version_managers_by_user(
            request=mock_request
        )

        # Assert
        self.assertTrue(item.user_id == user_id for item in result)


class TestTypeVersionManagerGetActiveVersionManagersByUser(TestCase):
    """Test Type Version Manager Get Active Version Manager By User"""

    @patch.object(TypeVersionManager, "get_active_version_manager_by_user_id")
    def test_get_active_version_managers_by_user_returns_types_with_given_user_id(
        self, mock_get_active_version_manager_by_user_id
    ):
        """test_get_version_managers_by_user_returns_types_with_given_user_id"""

        # Arrange
        user_id = "10"
        mock_user = create_mock_user(user_id=user_id, is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type1 = _create_mock_type_version_manager(user=user_id)
        mock_type2 = _create_mock_type_version_manager(user=user_id)

        mock_get_active_version_manager_by_user_id.return_value = [
            mock_type1,
            mock_type2,
        ]

        result = version_manager_api.get_active_version_manager_by_user_id(
            request=mock_request
        )

        # Assert
        self.assertTrue(item.user_id == user_id for item in result)


class TestTypeVersionManagerGetAllVersionManagers(TestCase):
    """Test Type Version Manager Get All Version Manager"""

    @patch.object(TypeVersionManager, "get_all_type_version_manager")
    def test_get_all_version_manager_by_user_returns_types(
        self, mock_get_all_type_version_manager
    ):
        """test_get_all_version_managers_by_user_returns_types"""

        # Arrange
        user_id = "10"
        mock_user = create_mock_user(user_id=user_id, is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type1 = _create_mock_type_version_manager(user=user_id)

        mock_get_all_type_version_manager.return_value = [mock_type1]

        result = version_manager_api.get_all_version_manager(
            request=mock_request
        )

        # Assert
        self.assertTrue(item.user_id == user_id for item in result)


class TestGetNoBucketsTypes(TestCase):
    """Test Get No Buckets Types"""

    @patch.object(TypeVersionManager, "get_global_version_managers")
    @patch.object(Bucket, "get_all")
    def test_get_no_buckets_types_returns_types(
        self, mock_get_all_buckets, mock_get_global_version_managers
    ):
        """test_get_no_buckets_types_returns_types"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_type1 = _create_mock_type_version_manager()
        mock_type2 = _create_mock_type_version_manager()
        mock_bucket = _create_mock_bucket(
            types=[_create_mock_type_version_manager()]
        )
        mock_get_global_version_managers.exclude.return_value = [
            mock_type1,
            mock_type2,
        ]
        mock_get_all_buckets.return_value = [mock_bucket]

        result = get_no_buckets_types(request=mock_request)
        self.assertTrue(
            all(isinstance(item, TypeVersionManager) for item in result)
        )


def _create_mock_bucket(types=None):
    """Returns a mock bucket

    Args:
        types:

    Returns:

    """
    if types is None:
        types = []
    mock_bucket = Mock(spec=Bucket)
    mock_bucket.label = "bucket"
    mock_bucket.label = "#000000"

    mock_bucket_types = MagicMock()
    mock_bucket_types.all.return_value = types
    mock_bucket.types = mock_bucket_types
    return mock_bucket


def _create_mock_type(filename="", content="", is_disable=False):
    """Returns a mock type

    Args:
        filename:
        content:
        is_disable:

    Returns:

    """
    mock_type = Mock(spec=Type)
    mock_type.filename = filename
    mock_type.content = content
    mock_type.id = 1
    mock_type.is_disabled = is_disable
    return mock_type


def _create_mock_type_version_manager(title="", versions=None, user="1"):
    """Returns a mock type version manager

    Args:
        title:
        versions:

    Returns:

    """
    mock_type_version_manager = Mock(spec=TypeVersionManager)
    mock_type_version_manager.title = title
    mock_type_version_manager.id = 1
    mock_type_version_manager.user = user
    if versions is not None:
        mock_type_version_manager.versions = versions
    else:
        mock_type_version_manager.versions = []
    mock_type_version_manager.disabled_versions = []
    return mock_type_version_manager


def _create_type(filename="test", content=None):
    """Returns a type

    Args:
        filename:
        content:

    Returns:

    """
    if content is None:
        # set a valid content
        content = (
            "<schema xmlns='http://www.w3.org/2001/XMLSchema'><simpleType name='type'>"
            "<restriction base='string'><enumeration value='test'/></restriction>"
            "</simpleType></schema>"
        )
    return Type(id=1, filename=filename, content=content)


def _create_type_version_manager(title="", user="1"):
    """Returns a type version manager

    Args:
        title:
        user:

    Returns:

    """
    return TypeVersionManager(
        id=1,
        title=title,
        user=user,
    )


class MockDependencies:
    """MockDependencies"""

    def clear(self):
        """Clear

        Returns:

        """
        pass


class MockTypes:
    """MockTypes"""

    def __init__(self, types):
        self._types = types

    def all(self):
        """All
        Returns:
        """
        return self._types

    def count(self):
        """Count
        Returns:
        """
        return len(self._types)
