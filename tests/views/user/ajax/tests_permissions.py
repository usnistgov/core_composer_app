""" Permission tests for AJAX views in `views.user` package.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.core.exceptions import PermissionDenied
from rest_framework import status

from core_composer_app.views.user import ajax
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestSaveTemplate(TestCase):
    """Permission tests for `save_template` method."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_request.POST = {"templateName": "mock_template"}
        self.mock_request.session = {
            "newXmlTemplateCompose": "mock_new_template_xml",
            "includedTypesCompose": ["mock_type"],
        }

    def test_anon_without_perm_raises_exception(self):
        """test_anon_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(None, is_anonymous=True)

        with self.assertRaises(PermissionDenied):
            ajax.save_template(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch("django.contrib.auth.models.Group.objects.filter")
    def test_anon_with_perm_returns_200(
        self,
        mock_anonymous_group,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_messages,
    ):
        """test_anon_with_perm_returns_200"""
        mock_anonymous_group.return_value = True
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(
            None, is_anonymous=True, has_perm=True
        )

        response = ajax.save_template(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_without_perm_raises_exception(self):
        """test_user_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(1)

        with self.assertRaises(PermissionDenied):
            ajax.save_template(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_user_with_perm_returns_200(
        self,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_messages,
    ):
        """test_user_with_perm_returns_200"""
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(1, has_perm=True)

        response = ajax.save_template(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_staff_without_perm_raises_exception(self):
        """test_staff_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(1, is_staff=True)

        with self.assertRaises(PermissionDenied):
            ajax.save_template(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_staff_with_perm_returns_200(
        self,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_messages,
    ):
        """test_staff_with_perm_returns_200"""
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(
            1, is_staff=True, has_perm=True
        )

        response = ajax.save_template(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_superuser_without_perm_raises_exception(self):
        """test_superuser_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(
            1, is_staff=True, is_superuser=True
        )

        with self.assertRaises(PermissionDenied):
            ajax.save_template(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_superuser_with_perm_returns_200(
        self,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_messages,
    ):
        """test_superuser_with_perm_returns_200"""
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(
            1, is_staff=True, is_superuser=True, has_perm=True
        )

        response = ajax.save_template(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class TestSaveType(TestCase):
    """Permission tests for `save_type` method."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_request.POST = {"typeName": "mock_type", "templateID": "new"}
        self.mock_request.session = {
            "newXmlTemplateCompose": "mock_new_template_xml",
            "includedTypesCompose": ["mock_type"],
        }

    def test_anon_without_perm_raises_exception(self):
        """test_anon_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(None, is_anonymous=True)

        with self.assertRaises(PermissionDenied):
            ajax.save_type(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    @patch("django.contrib.auth.models.Group.objects.filter")
    def test_anon_with_perm_returns_200(
        self,
        mock_anonymous_group,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_anon_with_perm_returns_200"""
        mock_anonymous_group.return_value = True
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(
            None, is_anonymous=True, has_perm=True
        )

        response = ajax.save_type(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_without_perm_raises_exception(self):
        """test_user_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(1)

        with self.assertRaises(PermissionDenied):
            ajax.save_type(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_user_with_perm_returns_200(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_user_with_perm_returns_200"""
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(1, has_perm=True)

        response = ajax.save_type(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_staff_without_perm_raises_exception(self):
        """test_staff_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(1, is_staff=True)

        with self.assertRaises(PermissionDenied):
            ajax.save_type(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_staff_with_perm_returns_200(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_staff_with_perm_returns_200"""
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(
            1, is_staff=True, has_perm=True
        )

        response = ajax.save_type(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_superuser_without_perm_raises_exception(self):
        """test_superuser_without_perm_raises_exception"""
        self.mock_request.user = create_mock_user(
            1, is_staff=True, is_superuser=True
        )

        with self.assertRaises(PermissionDenied):
            ajax.save_type(self.mock_request)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_superuser_with_perm_returns_200(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_superuser_with_perm_returns_200"""
        mock_main_utils.validate_xml_schema.return_value = None
        self.mock_request.user = create_mock_user(
            1, is_staff=True, is_superuser=True, has_perm=True
        )

        response = ajax.save_type(self.mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
