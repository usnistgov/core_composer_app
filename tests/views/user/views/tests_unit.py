""" Unit tests for user views
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_composer_app.views.user import views as user_views


class TestBuildTemplate(TestCase):
    """Unit tests for `build_template` view."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_request.user = create_mock_user(1, has_perm=True)

    @patch.object(user_views, "render")
    @patch.object(user_views, "get_xsd_types")
    @patch.object(user_views, "bucket_api")
    @patch.object(user_views, "type_version_manager_api")
    @patch.object(user_views, "xsl_transform")
    @patch.object(user_views, "read_file_content")
    @patch.object(user_views, "finders")
    @patch.object(user_views, "remove_annotations")
    @patch.object(user_views, "XSDTree")
    @patch.object(user_views, "template_api")
    def test_context_correctly_built(
        self,
        mock_template_api,
        mock_xsd_tree,
        mock_remove_annotations,
        mock_finders,
        mock_read_file_content,
        mock_xsl_transform,
        mock_type_version_manager_api,
        mock_bucket_api,
        mock_get_xsd_types,
        mock_render,
    ):
        """test_context_correctly_built"""
        mock_template_id = 1
        mock_xsd_form = "mock_xsd_form"
        mock_user_types = ["mock_user_type_1", "mock_user_type_2"]

        mock_bucket_1_types = MagicMock()
        mock_bucket_1_types_filtered = ["mock_type_11", "mock_type_12"]
        mock_bucket_1_types.filter.return_value = mock_bucket_1_types_filtered
        mock_bucket_1 = MagicMock()
        mock_bucket_1.label = "mock_bucket_1"
        mock_bucket_1.color = "mock_bucket_1_color"
        mock_bucket_1.types = mock_bucket_1_types

        mock_bucket_2_types = MagicMock()
        mock_bucket_2_types_filtered = ["mock_type_21"]
        mock_bucket_2_types.filter.return_value = mock_bucket_2_types_filtered
        mock_bucket_2 = MagicMock()
        mock_bucket_2.label = "mock_bucket_2"
        mock_bucket_2.color = "mock_bucket_2_color"
        mock_bucket_2.types = mock_bucket_2_types

        mock_buckets = [mock_bucket_1, mock_bucket_2]

        mock_no_bucket_types = [
            "mock_no_bucket_type_1",
            "mock_no_bucket_type_2",
        ]
        mock_built_in_types = [
            "mock_no_bucket_type_1",
            "mock_no_bucket_type_2",
        ]

        mock_xsl_transform.return_value = mock_xsd_form
        mock_type_version_manager_api.get_version_managers_by_user.filter.return_value = (
            mock_user_types
        )
        mock_bucket_api.get_all.return_value = mock_buckets
        mock_type_version_manager_api.get_no_buckets_types.filter.return_value = (
            mock_no_bucket_types
        )
        mock_get_xsd_types.return_value = mock_built_in_types
        mock_template_api.get_by_id.return_value = MagicMock(format="XSD")

        expected_context = {
            "buckets": [
                {
                    "label": mock_bucket_1.label,
                    "color": mock_bucket_1.color,
                    "types": mock_bucket_1_types_filtered,
                },
                {
                    "label": mock_bucket_2.label,
                    "color": mock_bucket_2.color,
                    "types": mock_bucket_2_types_filtered,
                },
            ],
            "built_in_types": [
                {"current": "built_in_type", "title": built_in_type}
                for built_in_type in mock_built_in_types
            ],
            "no_buckets_types": mock_type_version_manager_api.get_no_buckets_types().filter(),
            "user_types": mock_type_version_manager_api.get_version_managers_by_user().filter(),
            "xsd_form": mock_xsd_form,
            "template_id": mock_template_id,
            "page_title": "Build Template",
        }

        user_views.build_template(self.mock_request, mock_template_id)
        mock_render.assert_called_with(
            self.mock_request,
            "core_composer_app/user/build_template.html",
            **{
                "assets": {
                    "js": [
                        {
                            "path": "core_composer_app/user/js/build_template.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_composer_app/user/js/build_template.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_composer_app/user/js/xpath.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_composer_app/user/js/menus.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_composer_app/user/js/xsd_tree.js",
                            "is_raw": False,
                        },
                    ],
                    "css": [
                        "core_main_app/common/css/XMLTree.css",
                        "core_composer_app/common/css/bucket.css",
                        "core_composer_app/user/css/menu.css",
                        "core_composer_app/user/css/style.css",
                        "core_composer_app/user/css/xsd_tree.css",
                    ],
                },
                "context": expected_context,
                "modals": [
                    "core_composer_app/user/builder/menus/sequence.html",
                    "core_composer_app/user/builder/menus/element.html",
                    "core_composer_app/user/builder/menus/element_root.html",
                    "core_composer_app/user/builder/modals/root_type_name.html",
                    "core_composer_app/user/builder/modals/element_name.html",
                    "core_composer_app/user/builder/modals/insert_element.html",
                    "core_composer_app/user/builder/modals/delete_element.html",
                    "core_composer_app/user/builder/modals/change_type.html",
                    "core_composer_app/user/builder/modals/save_template.html",
                    "core_composer_app/user/builder/modals/save_type.html",
                    "core_composer_app/user/builder/modals/occurrences.html",
                    "core_composer_app/user/builder/modals/errors.html",
                ],
            },
        )

    @patch.object(user_views, "template_api")
    def test_build_with_bad_template_format_returns_error_page(
        self,
        mock_template_api,
    ):
        """test_build_with_bad_template_format_returns_error_page"""
        mock_template_id = 1
        mock_template_api.get_by_id.return_value = MagicMock(format="JSON")

        response = user_views.build_template(
            self.mock_request, mock_template_id
        )
        self.assertTrue(
            "Template format not supported." in response.content.decode()
        )
