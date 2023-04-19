""" Access control testing
"""

from django.test import override_settings

from core_main_app.access_control.exceptions import AccessControlError
from core_composer_app.components.type_version_manager import (
    api as type_vm_api,
)
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_composer_app.components.type_version_manager.models import (
    TypeVersionManager,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

from tests.components.type_version_manager.fixtures.fixtures import (
    TypeVersionManagerFixtures,
    TypeVersionManagerAccessControlFixtures,
)

fixture_type_vm = TypeVersionManagerFixtures()
fixture_type_vm2 = TypeVersionManagerAccessControlFixtures()


class TestTypeVersionManagerGet(IntegrationBaseTestCase):
    """TestTypeVersionManagerGet"""

    fixture = fixture_type_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.staff_user1 = create_mock_user(user_id="2", is_staff=True)
        self.superuser1 = create_mock_user(user_id="2", is_superuser=True)
        self.fixture.insert_data()

    def test_get_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_by_id(
                self.fixture.type_vm_2.id, request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_user_version_manager_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test get user version manager as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_by_id(
                self.fixture.type_vm_2.id, request=mock_request
            )

    def test_get_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_by_id(
                self.fixture.type_vm_1.id, request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_global_version_manager_as_anonymous_with_access_right_returns_global_type(
        self,
    ):
        """test get global version manager as anonymous with access right returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        version_manager = type_vm_api.get_by_id(
            self.fixture.type_vm_1.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.type_vm_1)

    def test_get_own_version_manager_as_user_returns_version_manager(self):
        """test get own version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = type_vm_api.get_by_id(
            self.fixture.type_vm_2.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.type_vm_2)

    def test_global_version_manager_as_user_returns_version_manager(self):
        """test global version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = type_vm_api.get_by_id(
            self.fixture.type_vm_1.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.type_vm_1)

    def test_get_other_users_version_manager_raises_access_control_error(self):
        """test get other users version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user2)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_by_id(
                self.fixture.type_vm_2.id, request=mock_request
            )

    def test_get_any_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        """test get any version manager as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = type_vm_api.get_by_id(
            self.fixture.type_vm_2.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.type_vm_2)

    def test_get_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test get other users version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_by_id(
                self.fixture.type_vm_2.id, request=mock_request
            )


class TestTypeVersionManagerGetActiveGlobalVersionManager(
    IntegrationBaseTestCase
):
    """TestTypeVersionManagerGetActiveGlobalVersionManager"""

    fixture = fixture_type_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get active global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_active_global_version_manager(request=mock_request)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_active_global_version_manager_as_anonymous_with_access_right_returns_version_manager(
        self,
    ):
        """test get active global version manager as anonymous with access right returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        version_manager = type_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        self.assertTrue(self.fixture.type_vm_1 in version_manager)

    def test_get_active_global_version_manager_as_user_returns_version_manager(
        self,
    ):
        """test get active global version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = type_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        self.assertTrue(self.fixture.type_vm_1 in version_manager)

    def test_get_active_global_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        """test get active global version manager as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = type_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        self.assertTrue(self.fixture.type_vm_1 in version_manager)

    def test_get_active_global_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test get active global version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = type_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        self.assertTrue(self.fixture.type_vm_1 in version_manager)


class TestTypeVersionManagerInsert(IntegrationBaseTestCase):
    """TestTypeVersionManagerInsert"""

    fixture = fixture_type_vm2

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_insert_user_type_as_anonymous_raises_access_control_error(self):
        """test insert user type as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.user1_tvm,
                self.fixture.user1_type,
                request=mock_request,
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_insert_user_type_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test insert user type as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.user1_tvm,
                self.fixture.user1_type,
                request=mock_request,
            )

    def test_insert_global_type_as_anonymous_raises_access_control_error(self):
        """test insert global type as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_type,
                request=mock_request,
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_insert_global_type_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test insert global type as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_type,
                request=mock_request,
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_own_type_as_user_saves(self):
        """test insert own type as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        result = type_vm_api.insert(
            self.fixture.user1_tvm,
            self.fixture.user1_type,
            request=mock_request,
        )
        self.assertIsInstance(result, TypeVersionManager)

    def test_insert_other_users_type_as_user_raises_access_control_error(self):
        """test insert other users type as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.user2_tvm,
                self.fixture.user2_type,
                request=mock_request,
            )

    def test_insert_global_type_as_user_raises_access_control_error(self):
        """test insert global type as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_type,
                request=mock_request,
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_own_type_as_staff_saves(self):
        """test insert own type as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        result = type_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_type,
            request=mock_request,
        )

        self.assertIsInstance(result, TypeVersionManager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_other_users_type_as_staff_raises_access_control_error(
        self,
    ):
        """test insert other users type as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            type_vm_api.insert(
                self.fixture.user2_tvm,
                self.fixture.user2_type,
                request=mock_request,
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_global_type_as_staff_saves(self):
        """test insert global type as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        result = type_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_type,
            request=mock_request,
        )
        self.assertIsInstance(result, TypeVersionManager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_own_type_as_superuser_saves(self):
        """test insert own type as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        result = type_vm_api.insert(
            self.fixture.user1_tvm,
            self.fixture.user1_type,
            request=mock_request,
        )
        self.assertIsInstance(result, TypeVersionManager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_other_users_type_as_superuser_saves(self):
        """test insert other users type as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        result = type_vm_api.insert(
            self.fixture.user2_tvm,
            self.fixture.user2_type,
            request=mock_request,
        )

        self.assertIsInstance(result, TypeVersionManager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_insert_global_type_as_superuser_saves(self):
        """test insert global type as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        result = type_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_type,
            request=mock_request,
        )

        self.assertIsInstance(result, TypeVersionManager)


class TestTypeVersionManagerGetNoBucketsTypes(IntegrationBaseTestCase):
    """Test Type Version Manager Get No Buckets Types"""

    fixture = fixture_type_vm2

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.staff_user1 = create_mock_user(user_id="2", is_staff=True)
        self.superuser1 = create_mock_user(user_id="2", is_superuser=True)
        self.fixture.insert_data()

    def test_get_no_buckets_types_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get no buckets types as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_no_buckets_types(request=mock_request)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_no_buckets_types_as_anonymous_with_access_right_returns_types_without_buckets_only(
        self,
    ):
        """test get no buckets types as anonymous with access right returns types without buckets only

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)

        result = type_vm_api.get_no_buckets_types(request=mock_request)

        self.assertEqual(len(result), 1)

    def test_get_no_buckets_types_as_user_returns_types_without_buckets_only(
        self,
    ):
        """test get no buckets types as user returns types without buckets only

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)

        result = type_vm_api.get_no_buckets_types(request=mock_request)

        self.assertEqual(len(result), 1)

    def test_get_no_buckets_types_as_superuser_returns_types_without_buckets_only(
        self,
    ):
        """test get no buckets types as superuser returns types without buckets only

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)

        result = type_vm_api.get_no_buckets_types(request=mock_request)

        self.assertEqual(len(result), 1)

    def test_get_no_buckets_types_as_staff_returns_types_without_buckets_only(
        self,
    ):
        """test get no buckets types as staff returns types without buckets only

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)

        result = type_vm_api.get_no_buckets_types(request=mock_request)

        self.assertEqual(len(result), 1)


class TestTypeVersionManagerGetAllVersionManager(IntegrationBaseTestCase):
    """Test Type Version Manager Get All Version Manager"""

    fixture = fixture_type_vm2

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get all version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)

        with self.assertRaises(AccessControlError):
            type_vm_api.get_all_version_manager(request=mock_request)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_all_version_manager_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test get all version manager as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_all_version_manager(request=mock_request)

    def test_get_all_version_manager_as_user_raises_access_control_error(self):
        """test get all version manager as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_all_version_manager(request=mock_request)

    def test_get_all_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test get all version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            type_vm_api.get_all_version_manager(request=mock_request)

    def test_get_all_version_manager_as_superuser_returns_user_all_version_manager(
        self,
    ):
        """test get all version manager as superuser returns all version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)

        list_tvm = type_vm_api.get_all_version_manager(request=mock_request)

        self.assertEqual(len(list_tvm), 3)
