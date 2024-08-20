""" Unit tests for `core_composer_app.views.admin.views` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_composer_app.views.admin import views as composer_admin_views
from core_main_app.commons.exceptions import XSDError, NotUniqueError


class TestSaveType(TestCase):
    """Unit tests for `_save_type` view."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "request": MagicMock(),
            "assets": MagicMock(),
            "context": MagicMock(),
        }

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "HttpResponseRedirect")
    @patch.object(composer_admin_views, "reverse")
    def test_read_xsd_file_called(
        self,
        mock_reverse,
        mock_http_response_redirect,
        mock_type_version_manager_api,
        mock_read_xsd_file,
    ):
        """test_read_xsd_file_called"""
        composer_admin_views._save_type(**self.mock_kwargs)

        mock_read_xsd_file.assert_called_with(
            self.mock_kwargs["request"].FILES["xsd_file"]
        )

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "HttpResponseRedirect")
    @patch.object(composer_admin_views, "reverse")
    def test_post_getlist_called(
        self,
        mock_reverse,
        mock_http_response_redirect,
        mock_type_version_manager_api,
        mock_read_xsd_file,
    ):
        """test_post_getlist_called"""
        composer_admin_views._save_type(**self.mock_kwargs)

        self.mock_kwargs["request"].POST.getlist.assert_called_with("buckets")

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "Type")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "HttpResponseRedirect")
    @patch.object(composer_admin_views, "reverse")
    def test_type_instantiated(
        self,
        mock_reverse,
        mock_http_response_redirect,
        mock_type_version_manager_api,
        mock_type,
        mock_read_xsd_file,
    ):
        """test_type_instantiated"""
        mock_xsd_data = MagicMock()
        mock_read_xsd_file.return_value = mock_xsd_data

        composer_admin_views._save_type(**self.mock_kwargs)

        mock_type.assert_called_with(
            filename=self.mock_kwargs["request"].FILES["xsd_file"].name,
            content=mock_xsd_data,
        )

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "TypeVersionManager")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "HttpResponseRedirect")
    @patch.object(composer_admin_views, "reverse")
    def test_type_version_manager_instantiated(
        self,
        mock_reverse,
        mock_http_response_redirect,
        mock_type_version_manager_api,
        mock_type_version_manager,
        mock_read_xsd_file,
    ):
        """test_type_version_manager_instantiated"""
        composer_admin_views._save_type(**self.mock_kwargs)

        mock_type_version_manager.assert_called_with(
            title=self.mock_kwargs["request"].POST["name"]
        )

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "Type")
    @patch.object(composer_admin_views, "TypeVersionManager")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "HttpResponseRedirect")
    @patch.object(composer_admin_views, "reverse")
    def test_type_version_manager_api_insert_called(
        self,
        mock_reverse,
        mock_http_response_redirect,
        mock_type_version_manager_api,
        mock_type_version_manager,
        mock_type,
        mock_read_xsd_file,
    ):
        """test_type_version_manager_api_insert_called"""
        mock_type_object = MagicMock()
        mock_type.return_value = mock_type_object

        mock_type_version_manager_object = MagicMock()
        mock_type_version_manager.return_value = (
            mock_type_version_manager_object
        )

        composer_admin_views._save_type(**self.mock_kwargs)

        mock_type_version_manager_api.insert.assert_called_with(
            mock_type_version_manager_object,
            mock_type_object,
            request=self.mock_kwargs["request"],
            list_bucket_ids=self.mock_kwargs["request"].POST.getlist(
                "buckets"
            ),
        )

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "Type")
    @patch.object(composer_admin_views, "TypeVersionManager")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "HttpResponseRedirect")
    @patch.object(composer_admin_views, "reverse")
    def test_http_response_redirect_returned(
        self,
        mock_reverse,
        mock_http_response_redirect,
        mock_type_version_manager_api,
        mock_type_version_manager,
        mock_type,
        mock_read_xsd_file,
    ):
        """test_http_response_redirect_returned"""
        mock_reverse_object = MagicMock()
        mock_reverse.return_value = mock_reverse_object

        composer_admin_views._save_type(**self.mock_kwargs)

        mock_http_response_redirect.assert_called_with(mock_reverse_object)

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "Type")
    @patch.object(composer_admin_views, "TypeVersionManager")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "_handle_xsd_errors")
    def test_xsd_error_returns_handle_xsd_errors(
        self,
        mock_handle_xsd_errors,
        mock_type_version_manager_api,
        mock_type_version_manager,
        mock_type,
        mock_read_xsd_file,
    ):
        """test_xsd_error_returns_handle_xsd_errors"""
        mock_xsd_data = MagicMock()
        mock_read_xsd_file.return_value = mock_xsd_data

        mock_xsd_error = XSDError("mock_read_xsd_file_xsd_error")
        mock_type.side_effect = mock_xsd_error

        expected_result = MagicMock()
        mock_handle_xsd_errors.return_value = expected_result

        self.assertEqual(
            composer_admin_views._save_type(**self.mock_kwargs),
            expected_result,
        )

        mock_handle_xsd_errors.assert_called_with(
            self.mock_kwargs["request"],
            self.mock_kwargs["assets"],
            self.mock_kwargs["context"],
            mock_xsd_error,
            mock_xsd_data,
            self.mock_kwargs["request"].FILES["xsd_file"].name,
        )

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "Type")
    @patch.object(composer_admin_views, "TypeVersionManager")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "_upload_type_response")
    def test_not_unique_error_returns_upload_type_response(
        self,
        mock_upload_type_response,
        mock_type_version_manager_api,
        mock_type_version_manager,
        mock_type,
        mock_read_xsd_file,
    ):
        """test_not_unique_error_returns_upload_type_response"""
        mock_read_xsd_file.side_effect = NotUniqueError(
            "mock_read_xsd_file_not_unique_error"
        )

        expected_result = MagicMock()
        mock_upload_type_response.return_value = expected_result

        self.assertEqual(
            composer_admin_views._save_type(**self.mock_kwargs),
            expected_result,
        )

        mock_upload_type_response.assert_called_with(
            self.mock_kwargs["request"],
            self.mock_kwargs["assets"],
            self.mock_kwargs["context"],
        )

    @patch.object(composer_admin_views, "read_xsd_file")
    @patch.object(composer_admin_views, "Type")
    @patch.object(composer_admin_views, "TypeVersionManager")
    @patch.object(composer_admin_views, "type_version_manager_api")
    @patch.object(composer_admin_views, "_upload_type_response")
    def test_exception_returns_upload_type_response(
        self,
        mock_upload_type_response,
        mock_type_version_manager_api,
        mock_type_version_manager,
        mock_type,
        mock_read_xsd_file,
    ):
        """test_exception_returns_upload_type_response"""
        mock_read_xsd_file.side_effect = Exception(
            "mock_read_xsd_file_exception"
        )
        expected_result = MagicMock()
        mock_upload_type_response.return_value = expected_result

        self.assertEqual(
            composer_admin_views._save_type(**self.mock_kwargs),
            expected_result,
        )

        mock_upload_type_response.assert_called_with(
            self.mock_kwargs["request"],
            self.mock_kwargs["assets"],
            self.mock_kwargs["context"],
        )


class TestUploadBucketPost(TestCase):
    """Unit tests for `upload_bucket` view, limited to POST requests."""

    def setUp(self):
        """setUp"""
        self.request = MagicMock()
        self.request.method = "POST"
        self.mock_kwargs = {"request": self.request}

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "admin_render")
    def test_bucket_form_instantiated(
        self, mock_admin_render, mock_bucket_form
    ):
        """test_bucket_form_instantiated"""
        composer_admin_views.upload_bucket(**self.mock_kwargs)

        mock_bucket_form.assert_called_with(self.mock_kwargs["request"].POST)

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "admin_render")
    def test_invalid_form_returns_admin_render(
        self, mock_admin_render, mock_bucket_form
    ):
        """test_invalid_form_returns_admin_render"""
        mock_bucket_form_object = MagicMock()
        mock_bucket_form_object.is_valid.return_value = False
        mock_bucket_form.return_value = mock_bucket_form_object

        expected_result = MagicMock()
        mock_admin_render.return_value = expected_result

        self.assertEqual(
            composer_admin_views.upload_bucket(**self.mock_kwargs),
            expected_result,
        )

        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_composer_app/admin/buckets/add.html",
            context={"object_name": "Bucket", "form": mock_bucket_form_object},
            assets={
                "js": [
                    {
                        "path": "core_main_app/common/js/backtoprevious.js",
                        "is_raw": True,
                    }
                ]
            },
        )

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "Bucket")
    @patch.object(composer_admin_views, "redirect")
    @patch.object(composer_admin_views, "reverse")
    def test_bucket_object_instantiated(
        self, mock_reverse, mock_redirect, mock_bucket, mock_bucket_form
    ):
        """test_bucket_object_instantiated"""
        composer_admin_views.upload_bucket(**self.mock_kwargs)

        mock_bucket.assert_called_with(
            label=self.mock_kwargs["request"].POST["label"]
        )

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "Bucket")
    @patch.object(composer_admin_views, "bucket_api")
    @patch.object(composer_admin_views, "redirect")
    @patch.object(composer_admin_views, "reverse")
    def test_bucket_api_upsert_called(
        self,
        mock_reverse,
        mock_redirect,
        mock_bucket_api,
        mock_bucket,
        mock_bucket_form,
    ):
        """test_bucket_api_upsert_called"""
        mock_bucket_object = MagicMock()
        mock_bucket.return_value = mock_bucket_object

        composer_admin_views.upload_bucket(**self.mock_kwargs)

        mock_bucket_api.upsert.assert_called_with(mock_bucket_object)

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "Bucket")
    @patch.object(composer_admin_views, "bucket_api")
    @patch.object(composer_admin_views, "redirect")
    @patch.object(composer_admin_views, "reverse")
    def test_success_returns_redirect(
        self,
        mock_reverse,
        mock_redirect,
        mock_bucket_api,
        mock_bucket,
        mock_bucket_form,
    ):
        """test_success_returns_redirect"""
        mock_reverse_obj = MagicMock()
        mock_reverse.return_value = mock_reverse_obj

        expected_result = MagicMock()
        mock_redirect.return_value = expected_result

        self.assertEqual(
            composer_admin_views.upload_bucket(**self.mock_kwargs),
            expected_result,
        )

        mock_redirect.assert_called_with(mock_reverse_obj)

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "Bucket")
    @patch.object(composer_admin_views, "bucket_api")
    @patch.object(composer_admin_views, "admin_render")
    def test_not_unique_error_returns_admin_render(
        self, mock_admin_render, mock_bucket_api, mock_bucket, mock_bucket_form
    ):
        """test_not_unique_error_returns_admin_render"""
        mock_bucket_form_obj = MagicMock()
        mock_bucket_form.return_value = mock_bucket_form_obj

        mock_bucket_api.upsert.side_effect = NotUniqueError(
            "mock_bucket_api_upsert_not_unique_error"
        )

        expected_result = MagicMock()
        mock_admin_render.return_value = expected_result

        self.assertEqual(
            composer_admin_views.upload_bucket(**self.mock_kwargs),
            expected_result,
        )

        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_composer_app/admin/buckets/add.html",
            context={
                "object_name": "Bucket",
                "errors": "A bucket with the same name already exists.",
                "form": mock_bucket_form_obj,
            },
            assets={
                "js": [
                    {
                        "path": "core_main_app/common/js/backtoprevious.js",
                        "is_raw": True,
                    }
                ]
            },
        )

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "Bucket")
    @patch.object(composer_admin_views, "bucket_api")
    @patch.object(composer_admin_views, "admin_render")
    def test_exception_returns_admin_render(
        self, mock_admin_render, mock_bucket_api, mock_bucket, mock_bucket_form
    ):
        """test_exception_returns_admin_render"""
        mock_bucket_form_obj = MagicMock()
        mock_bucket_form.return_value = mock_bucket_form_obj

        mock_bucket_api.upsert.side_effect = Exception(
            "mock_bucket_api_upsert_exception"
        )

        expected_result = MagicMock()
        mock_admin_render.return_value = expected_result

        self.assertEqual(
            composer_admin_views.upload_bucket(**self.mock_kwargs),
            expected_result,
        )

        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_composer_app/admin/buckets/add.html",
            context={
                "object_name": "Bucket",
                "errors": "mock_bucket_api_upsert_exception",
                "form": mock_bucket_form_obj,
            },
            assets={
                "js": [
                    {
                        "path": "core_main_app/common/js/backtoprevious.js",
                        "is_raw": True,
                    }
                ]
            },
        )


class TestUploadBucketGet(TestCase):
    """Unit tests for `upload_bucket` view, limited to GET requests."""

    def setUp(self):
        """setUp"""
        self.request = MagicMock()
        self.request.method = "GET"
        self.mock_kwargs = {"request": self.request}

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "admin_render")
    def test_bucket_form_instantiated(
        self, mock_admin_render, mock_bucket_form
    ):
        """test_bucket_form_instantiated"""
        composer_admin_views.upload_bucket(**self.mock_kwargs)

        mock_bucket_form.assert_called_with()

    @patch.object(composer_admin_views, "BucketForm")
    @patch.object(composer_admin_views, "admin_render")
    def test_admin_render_returns(self, mock_admin_render, mock_bucket_form):
        """test_admin_render_returns"""
        mock_bucket_form_object = MagicMock()
        mock_bucket_form.return_value = mock_bucket_form_object

        expected_value = MagicMock()
        mock_admin_render.return_value = expected_value

        self.assertEqual(
            composer_admin_views.upload_bucket(**self.mock_kwargs),
            expected_value,
        )

        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_composer_app/admin/buckets/add.html",
            context={"object_name": "Bucket", "form": mock_bucket_form_object},
            assets={
                "js": [
                    {
                        "path": "core_main_app/common/js/backtoprevious.js",
                        "is_raw": True,
                    }
                ]
            },
        )
