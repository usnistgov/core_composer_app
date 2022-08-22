"""Bucket test cases
"""
from unittest.case import TestCase

from mock.mock import Mock, patch

from core_main_app.commons import exceptions
from core_composer_app.components.bucket import api as bucket_api
from core_composer_app.components.bucket.models import Bucket
from core_composer_app.components.type_version_manager.models import TypeVersionManager


class TestBucketGetById(TestCase):
    """Test Bucket Get By Id"""

    @patch.object(Bucket, "get_by_id")
    def test_bucket_get_by_id_returns_bucket(self, mock_get_by_id):
        """test_bucket_get_by_id_returns_bucket"""

        # Arrange
        mock_bucket = _create_mock_bucket()

        mock_get_by_id.return_value = mock_bucket

        # Act
        result = bucket_api.get_by_id(mock_bucket.id)

        # Assert
        self.assertIsInstance(result, Bucket)

    @patch.object(Bucket, "get_by_id")
    def test_bucket_get_by_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test_bucket_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = -1
        mock_get_by_id.side_effect = exceptions.DoesNotExist("")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            bucket_api.get_by_id(mock_absent_id)


class TestBucketUpsert(TestCase):
    """Test Bucket Upsert"""

    @patch.object(Bucket, "get_colors")
    @patch.object(Bucket, "save")
    def test_upsert_bucket_creates_bucket(self, mock_save, mock_get_colors):
        """test_upsert_bucket_creates_bucket"""

        bucket = _create_bucket()

        mock_save.return_value = bucket
        mock_get_colors.return_value = []
        bucket_api.upsert(bucket)
        self.assertIsInstance(bucket, Bucket)


class TestBucketGetAll(TestCase):
    """Test Bucket Get All"""

    @patch.object(Bucket, "get_all")
    def test_get_all_buckets_returns_buckets(self, mock_get_all):
        """test_get_all_buckets_returns_buckets"""

        # Arrange
        mock_bucket1 = _create_mock_bucket()
        mock_bucket2 = _create_mock_bucket()

        mock_get_all.return_value = [mock_bucket1, mock_bucket2]

        # Act
        result = bucket_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, Bucket) for item in result))


class TestAddTypeToBuckets(TestCase):
    """Test Add Type To Buckets"""

    @patch.object(Bucket, "add_type")
    @patch.object(Bucket, "get_by_id")
    @patch.object(Bucket, "get_colors")
    @patch.object(Bucket, "save")
    def test_add_type_to_buckets_does_not_raise_error(
        self, mock_save, mock_get_colors, mock_get_by_id, mock_add_type
    ):
        """test_add_type_to_buckets_does_not_raise_error"""

        bucket = _create_bucket()
        mock_save.return_value = bucket
        mock_get_by_id.return_value = bucket
        mock_get_colors.return_value = []
        mock_add_type.return_value = None

        mock_version_manager = _create_mock_type_version_manager()

        bucket_api.add_type_to_buckets(mock_version_manager, [bucket.id])

    @patch.object(Bucket, "get_by_id")
    @patch.object(Bucket, "get_colors")
    @patch.object(Bucket, "save")
    def test_add_no_type_to_buckets_does_not_update_bucket(
        self, mock_save, mock_get_colors, mock_get_by_id
    ):
        """test_add_no_type_to_buckets_does_not_update_bucket"""

        bucket = _create_bucket()
        mock_save.return_value = bucket
        mock_get_by_id.return_value = bucket
        mock_get_colors.return_value = []

        mock_version_manager = _create_mock_type_version_manager()

        self.assertTrue(bucket.types.count() == 0)
        bucket_api.add_type_to_buckets(mock_version_manager, [])
        self.assertTrue(bucket.types.count() == 0)

    @patch.object(Bucket, "get_by_id")
    @patch.object(Bucket, "get_colors")
    @patch.object(Bucket, "save")
    def test_add_type_to_buckets_raises_exception_if_bucket_id_not_found(
        self, mock_save, mock_get_colors, mock_get_by_id
    ):
        """test_add_type_to_buckets_raises_exception_if_bucket_id_not_found"""

        mock_get_by_id.side_effect = exceptions.DoesNotExist
        mock_get_colors.return_value = []

        mock_version_manager = _create_mock_type_version_manager()

        with self.assertRaises(exceptions.ApiError):
            bucket_api.add_type_to_buckets(mock_version_manager, [-1])


class TestRemoveTypeFromBuckets(TestCase):
    """Test Remove Type F rom Buckets"""

    @patch.object(Bucket, "remove_type")
    @patch.object(Bucket, "get_all")
    @patch.object(Bucket, "get_by_id")
    @patch.object(Bucket, "get_colors")
    @patch.object(Bucket, "save")
    def test_remove_type_from_buckets_does_not_raise_error(
        self, mock_save, mock_get_colors, mock_get_by_id, mock_get_all, mock_remove_type
    ):
        """test_remove_type_from_buckets_does_not_raise_error"""

        bucket = _create_bucket()
        mock_version_manager = _create_mock_type_version_manager()

        mock_remove_type.return_value = None
        mock_get_all.return_value = [bucket]

        mock_save.return_value = bucket
        mock_get_by_id.return_value = bucket
        mock_get_colors.return_value = []

        bucket_api.remove_type_from_buckets(mock_version_manager)

    @patch.object(Bucket, "remove_type")
    @patch.object(Bucket, "get_all")
    @patch.object(Bucket, "get_by_id")
    @patch.object(Bucket, "get_colors")
    @patch.object(Bucket, "save")
    def test_removes_absent_type_from_buckets_does_not_raise_error(
        self, mock_save, mock_get_colors, mock_get_by_id, mock_get_all, mock_remove_type
    ):
        """test_removes_absent_type_from_buckets_does_not_raise_error"""

        bucket = _create_bucket()
        # mock_version_manager = _create_mock_type_version_manager()
        mock_absent_version_manager = _create_mock_type_version_manager()

        # bucket.types = [mock_version_manager]
        mock_get_all.return_value = [bucket]

        mock_save.return_value = bucket
        mock_get_by_id.return_value = bucket
        mock_get_colors.return_value = []
        mock_remove_type.return_value = None

        bucket_api.remove_type_from_buckets(mock_absent_version_manager)


def _create_mock_bucket():
    """Returns a mock bucket

    Args:

    Returns:

    """
    mock_bucket = Mock(spec=Bucket)
    mock_bucket.label = "bucket"
    mock_bucket.color = "#000000"
    mock_bucket.types = []
    mock_bucket.id = 1
    return mock_bucket


def _create_bucket():
    """Returns a bucket

    Args:

    Returns:

    """
    return Bucket(id=1, label="bucket", color="#000000")


def _create_mock_type_version_manager(title="", versions=None, user="1"):
    """Returns a mock type version manager

    Args:
        title:
        versions:

    Returns:

    """
    mock_type_version_manager = TypeVersionManager()
    mock_type_version_manager.title = title
    mock_type_version_manager.id = 1
    mock_type_version_manager.user = user
    if versions is not None:
        mock_type_version_manager.version_set.set(versions)
    return mock_type_version_manager
