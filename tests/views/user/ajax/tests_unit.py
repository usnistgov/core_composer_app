""" Unit tests for user AJAX views.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponse

from core_composer_app.views.user import ajax
from core_main_app.commons.exceptions import NotUniqueError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestSaveTemplate(TestCase):
    """Unit tests for `save_template` AJAX view."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_request.user = create_mock_user(1, has_perm=True)
        self.mock_request.POST = {"templateName": "mock_template"}
        self.mock_request.session = {
            "newXmlTemplateCompose": "mock_new_template_xml",
            "includedTypesCompose": ["mock_type"],
        }

    def test_no_template_name_in_request_returns_http_bad_request(self):
        """test_no_template_name_in_request_returns_http_bad_request"""
        del self.mock_request.POST["templateName"]

        response = ajax.save_template(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_no_template_compose_in_session_returns_http_bad_request(self):
        """test_no_template_compose_in_session_returns_http_bad_request"""
        del self.mock_request.session["newXmlTemplateCompose"]

        response = ajax.save_template(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "XSDTree")
    def test_build_tree_exception_returns_error_response(
        self, mock_xsd_tree, mock_error_response
    ):
        """test_build_tree_exception_returns_error_response"""
        mock_xsd_tree.build_tree.side_effect = Exception(
            "mock_build_tree_exception"
        )

        ajax.save_template(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_validate_xml_schema_exception_returns_error_response(
        self, mock_xsd_tree, mock_main_xml_utils, mock_error_response
    ):
        """test_validate_xml_schema_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.side_effect = Exception(
            "mock_validate_xml_schema_exception"
        )

        ajax.save_template(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_validate_xml_schema_returns_not_none_returns_error_response(
        self, mock_xsd_tree, mock_main_xml_utils, mock_error_response
    ):
        """test_validate_xml_schema_returns_not_none_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = "mock_error"

        ajax.save_template(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_get_dependencies_id_exception_returns_http_bad_request(
        self, mock_xsd_tree, mock_main_xml_utils, mock_get_dependencies_ids
    ):
        """test_get_dependencies_id_exception_returns_http_bad_request"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_get_dependencies_ids.side_effect = Exception(
            "mock_get_dependencies_ids_exception"
        )

        response = ajax.save_template(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_template_version_manager_exception_returns_error_response(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_error_response,
    ):
        """test_template_version_manager_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_template_version_manager.side_effect = Exception(
            "mock_template_version_manager_exception"
        )

        ajax.save_template(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_template_version_manager_validation_error_returns_http_bad_request(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
    ):
        """test_template_version_manager_validation_error_returns_http_bad_request"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_template_version_manager.side_effect = ValidationError(
            "mock_template_version_manager_validation_error"
        )

        response = ajax.save_template(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_template_exception_returns_error_response(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_error_response,
    ):
        """test_template_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_template.side_effect = Exception("mock_template_exception")

        ajax.save_template(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_template_version_manager_api_insert_exception_returns_error_response(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_error_response,
    ):
        """test_template_version_manager_api_insert_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_template_version_manager_api.insert.side_effect = Exception(
            "mock_template_version_manager_api_exception"
        )

        ajax.save_template(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_template_version_manager_api_insert_not_unique_error_returns_http_bad_request(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_error_response,
    ):
        """test_template_version_manager_api_insert_not_unique_error_returns_http_bad_request"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_template_version_manager_api.insert.side_effect = NotUniqueError(
            "mock_template_version_manager_api_exception"
        )

        response = ajax.save_template(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_success_calls_messages_api(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_messages,
    ):
        """test_success_calls_messages_api"""
        mock_main_xml_utils.validate_xml_schema.return_value = None

        ajax.save_template(self.mock_request)
        mock_messages.add_message.assert_called()

    @patch.object(ajax, "messages")
    @patch.object(ajax, "template_version_manager_api")
    @patch.object(ajax, "Template")
    @patch.object(ajax, "TemplateVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    def test_success_returns_http_response(
        self,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_template_version_manager,
        mock_template,
        mock_template_version_manager_api,
        mock_messages,
    ):
        """test_success_returns_http_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None

        response = ajax.save_template(self.mock_request)
        self.assertIsInstance(response, HttpResponse)


class TestSaveType(TestCase):
    """Unit tests for `save_type` AJAX view."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_request.user = create_mock_user(1, has_perm=True)
        self.mock_request.POST = {"typeName": "mock_type", "templateID": "new"}
        self.mock_request.session = {
            "newXmlTemplateCompose": "mock_new_template_xml",
            "includedTypesCompose": ["mock_type"],
        }

    def test_no_type_name_in_request_returns_http_bad_request(self):
        """test_no_type_name_in_request_returns_http_bad_request"""
        del self.mock_request.POST["typeName"]

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_no_template_id_in_request_returns_http_bad_request(self):
        """test_no_template_id_in_request_returns_http_bad_request"""
        del self.mock_request.POST["templateID"]

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_no_template_compose_in_session_returns_http_bad_request(self):
        """test_no_template_compose_in_session_returns_http_bad_request"""
        del self.mock_request.session["newXmlTemplateCompose"]

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "type_api")
    def test_no_type_api_get_exception_returns_error_response(
        self, mock_type_api, mock_error_response
    ):
        """test_no_type_api_get_exception_returns_error_response"""
        self.mock_request.POST["templateID"] = 1
        mock_type_api.get.side_effect = Exception("mock_type_api_exception")

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "composer_xml_utils")
    def test_remove_single_root_element_exception_returns_error_response(
        self, mock_composer_xml_utils, mock_error_response
    ):
        """test_build_tree_exception_returns_error_response"""
        mock_composer_xml_utils.remove_single_root_element.side_effect = (
            Exception("mock_remove_single_root_element_exception")
        )

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_build_tree_exception_returns_error_response(
        self, mock_composer_xml_utils, mock_xsd_tree, mock_error_response
    ):
        """test_build_tree_exception_returns_error_response"""
        mock_xsd_tree.build_tree.side_effect = Exception(
            "mock_build_tree_exception"
        )

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_validate_xml_schema_exception_returns_error_response(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_error_response,
    ):
        """test_validate_xml_schema_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.side_effect = Exception(
            "mock_validate_xml_schema_exception"
        )

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_validate_xml_schema_returns_not_none_returns_error_response(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_error_response,
    ):
        """test_validate_xml_schema_returns_not_none_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = "mock_error"

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_get_dependencies_id_exception_returns_http_bad_request(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
    ):
        """test_get_dependencies_id_exception_returns_http_bad_request"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_get_dependencies_ids.side_effect = Exception(
            "mock_get_dependencies_ids_exception"
        )

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_type_version_manager_exception_returns_error_response(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_error_response,
    ):
        """test_type_version_manager_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_type_version_manager.side_effect = Exception(
            "mock_type_version_manager_exception"
        )

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_type_version_manager_validation_error_returns_http_bad_request(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
    ):
        """test_type_version_manager_validation_error_returns_http_bad_request"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_type_version_manager.side_effect = ValidationError(
            "mock_type_version_manager_validation_error"
        )

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_type_exception_returns_error_response(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_error_response,
    ):
        """test_type_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_type.side_effect = Exception("mock_type_exception")

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_type_version_manager_api_insert_exception_returns_error_response(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_error_response,
    ):
        """test_type_version_manager_api_insert_exception_returns_error_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_type_version_manager_api.insert.side_effect = Exception(
            "type_version_manager_api_exception"
        )

        ajax.save_type(self.mock_request)
        mock_error_response.assert_called()

    @patch.object(ajax, "_error_response")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_type_version_manager_api_insert_not_unique_error_returns_http_bad_request(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_error_response,
    ):
        """test_type_version_manager_api_insert_not_unique_error_returns_http_bad_request"""
        mock_main_xml_utils.validate_xml_schema.return_value = None
        mock_type_version_manager_api.insert.side_effect = NotUniqueError(
            "type_version_manager_api_exception"
        )

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_success_calls_messages_api(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_success_calls_messages_api"""
        mock_main_xml_utils.validate_xml_schema.return_value = None

        ajax.save_type(self.mock_request)
        mock_messages.add_message.assert_called()

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    def test_success_returns_http_response(
        self,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_success_returns_http_response"""
        mock_main_xml_utils.validate_xml_schema.return_value = None

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponse)

    @patch.object(ajax, "messages")
    @patch.object(ajax, "type_version_manager_api")
    @patch.object(ajax, "Type")
    @patch.object(ajax, "TypeVersionManager")
    @patch.object(ajax, "_get_dependencies_ids")
    @patch.object(ajax, "main_xml_utils")
    @patch.object(ajax, "XSDTree")
    @patch.object(ajax, "composer_xml_utils")
    @patch.object(ajax, "type_api")
    def test_success_with_editing_existing_type_returns_http_response(
        self,
        mock_type_api,
        mock_composer_xml_utils,
        mock_xsd_tree,
        mock_main_xml_utils,
        mock_get_dependencies_ids,
        mock_type_version_manager,
        mock_type,
        mock_type_version_manager_api,
        mock_messages,
    ):
        """test_success_returns_http_response"""
        self.mock_request.POST["templateID"] = 1
        mock_type_api.get.side_effect = Exception("mock_type_api_exception")
        mock_main_xml_utils.validate_xml_schema.return_value = None

        response = ajax.save_type(self.mock_request)
        self.assertIsInstance(response, HttpResponse)
