""" Integration Test for Bucket Rest API
"""

from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_composer_app.rest.bucket import views
from tests.components.bucket.fixtures.fixtures import BucketFixtures

fixture_bucket = BucketFixtures()


class TestBucketList(IntegrationBaseTestCase):
    """Test Bucket List"""

    fixture = fixture_bucket

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {"label": "label"}

    def test_get_returns_http_200(self):
        """test_get_returns_http_200"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BucketList.as_view(), user)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_buckets(self):
        """test_get_returns_all_buckets"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BucketList.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_get_by_correct_label_returns_one_bucket(self):
        """test_get_by_correct_label_returns_one_bucket"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BucketList.as_view(),
            user,
            data={"label": self.fixture.bucket_1.label},
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_by_correct_label_returns_correct_bucket(self):
        """test_get_by_correct_label_returns_correct_bucket"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BucketList.as_view(),
            user,
            data={"label": self.fixture.bucket_1.label},
        )

        # Assert
        self.assertEqual(
            response.data[0]["label"], self.fixture.bucket_1.label
        )

    def test_get_by_incorrect_label_returns_no_bucket(self):
        """test_get_by_incorrect_label_returns_no_bucket"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BucketList.as_view(), user, data={"label": "incorrect label"}
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_returns_http_201(self):
        """test_post_returns_http_201"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_as_user_returns_http_403(self):
        """test_post_as_user_returns_http_403"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_empty_types_returns_http_201(self):
        """test_post_empty_types_returns_http_201"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data["types"] = []

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_one_correct_type_returns_http_201(self):
        """test_post_with_one_correct_type_returns_http_201"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data["types"] = [str(self.fixture.type_vm_1.id)]

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_one_correct_type_returns_response_containing_one_type(
        self,
    ):
        """test_post_with_one_correct_type_returns_response_containing_one_type"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data["types"] = [str(self.fixture.type_vm_1.id)]

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data["types"]), 1)

    def test_post_with_two_correct_type_returns_http_201(self):
        """test_post_with_two_correct_type_returns_http_201"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data["types"] = [
            str(self.fixture.type_vm_1.id),
            str(self.fixture.type_vm_2.id),
        ]

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_one_correct_type_returns_response_containing_two_types(
        self,
    ):
        """test_post_with_one_correct_type_returns_response_containing_two_types"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data["types"] = [
            str(self.fixture.type_vm_1.id),
            str(self.fixture.type_vm_2.id),
        ]

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data["types"]), 2)

    def test_post_with_one_incorrect_type_returns_http_400(self):
        """test_post_with_one_incorrect_type_returns_http_400"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data["types"] = ["wrong_type_id"]

        # Act
        response = RequestMock.do_request_post(
            views.BucketList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBucketDetail(IntegrationBaseTestCase):
    """Test Bucket Detail"""

    fixture = fixture_bucket

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {"label": "label"}

    def test_get_returns_http_200(self):
        """test_get_returns_http_200"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BucketDetail.as_view(),
            user,
            param={"pk": str(self.fixture.bucket_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_bucket(self):
        """test_get_returns_bucket"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BucketDetail.as_view(),
            user,
            param={"pk": str(self.fixture.bucket_1.id)},
        )

        # Assert
        self.assertEqual(response.data["label"], self.fixture.bucket_1.label)

    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BucketDetail.as_view(), user, param={"pk": -1}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_returns_http_204(self):
        """test_delete_returns_http_204"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_delete(
            views.BucketDetail.as_view(),
            user,
            param={"pk": str(self.fixture.bucket_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_wrong_id_returns_http_404(self):
        """test_delete_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_delete(
            views.BucketDetail.as_view(), user, param={"pk": -1}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.BucketDetail.as_view(),
            user,
            param={"pk": str(self.fixture.bucket_1.id)},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_returns_updated_label(self):
        """test_patch_returns_updated_label"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.BucketDetail.as_view(),
            user,
            param={"pk": str(self.fixture.bucket_1.id)},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.data["label"], self.data["label"])

    def test_patch_wrong_id_returns_http_404(self):
        """test_patch_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.BucketDetail.as_view(), user, param={"pk": -1}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTypeVersionManagerBuckets(IntegrationBaseTestCase):
    """Test Type Version Manager Buckets"""

    fixture = fixture_bucket

    def setUp(self):
        """setUp"""

        super().setUp()

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data = [{"id": str(self.fixture.bucket_1.id)}]

        # Act
        response = RequestMock.do_request_patch(
            views.TypeVersionManagerBuckets.as_view(),
            user,
            param={"pk": self.fixture.type_vm_1.id},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_two_correct_bucket_id_returns_http_200(self):
        """test_patch_two_correct_bucket_id_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data = [
            {"id": str(self.fixture.bucket_1.id)},
            {"id": str(self.fixture.bucket_2.id)},
        ]

        # Act
        response = RequestMock.do_request_patch(
            views.TypeVersionManagerBuckets.as_view(),
            user,
            param={"pk": self.fixture.type_vm_1.id},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_no_bucket_id_returns_http_200(self):
        """test_patch_no_bucket_id_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data = []

        # Act
        response = RequestMock.do_request_patch(
            views.TypeVersionManagerBuckets.as_view(),
            user,
            param={"pk": self.fixture.type_vm_1.id},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_bucket_id_returns_http_404(self):
        """test_patch_wrong_bucket_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data = [{"id": -1}]

        # Act
        response = RequestMock.do_request_patch(
            views.TypeVersionManagerBuckets.as_view(),
            user,
            param={"pk": self.fixture.type_vm_1.id},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wrong_template_version_manager_id_returns_http_404(self):
        """test_patch_wrong_template_version_manager_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.data = [{"id": str(self.fixture.bucket_1.id)}]

        # Act
        response = RequestMock.do_request_patch(
            views.TypeVersionManagerBuckets.as_view(),
            user,
            param={"pk": -1},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_other_user_type_version_manager_returns_http_403(self):
        """test_patch_other_user_type_version_manager_returns_http_403"""

        # Arrange
        user = create_mock_user("2")
        self.data = [{"id": str(self.fixture.bucket_1.id)}]

        # Act
        response = RequestMock.do_request_patch(
            views.TypeVersionManagerBuckets.as_view(),
            user,
            param={"pk": self.fixture.type_vm_1.id},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
