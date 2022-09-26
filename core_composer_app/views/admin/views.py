"""Composer admin views
"""
import logging

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.utils.html import escape as html_escape

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import (
    NotUniqueError,
    ModelError,
    DoesNotExist,
)
from core_main_app.utils.rendering import admin_render
from core_main_app.utils.xml import get_imports_and_includes
from core_main_app.views.admin.forms import UploadVersionForm
from core_main_app.views.common.views import read_xsd_file
from core_main_app.views.user.views import get_context_manage_template_versions

from core_composer_app.components.bucket import api as bucket_api
from core_composer_app.components.bucket.models import Bucket
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager import (
    api as type_version_manager_api,
)
from core_composer_app.components.type_version_manager.models import (
    TypeVersionManager,
)
from core_composer_app.views.admin.ajax import EditBucketView
from core_composer_app.views.admin.forms import (
    BucketForm,
    UploadTypeForm,
    EditTypeBucketsForm,
)
from core_composer_app.views.user.ajax import EditTypeVersionManagerView


logger = logging.getLogger(__name__)


@staff_member_required
def manage_types(request):
    """View that allows type management.

    Args:
        request:

    Returns:

    """
    # get all types
    type_version_managers = (
        type_version_manager_api.get_global_version_managers(request=request)
    )

    context = {
        "object_name": "Type",
        "available": [
            type_version_manager
            for type_version_manager in type_version_managers
            if not type_version_manager.is_disabled
        ],
        "disabled": [
            type_version_manager
            for type_version_manager in type_version_managers
            if type_version_manager.is_disabled
        ],
    }

    assets = {
        "js": [
            {
                "path": "core_main_app/common/js/templates/list/restore.js",
                "is_raw": False,
            },
            {
                "path": "core_main_app/common/js/templates/list/modals/disable.js",
                "is_raw": False,
            },
            EditTypeVersionManagerView.get_modal_js_path(),
        ],
        "css": ["core_composer_app/common/css/bucket.css"],
    }

    modals = [
        "core_main_app/admin/templates/list/modals/disable.html",
        EditTypeVersionManagerView.get_modal_html_path(),
    ]

    return admin_render(
        request,
        "core_composer_app/admin/types/list.html",
        assets=assets,
        context=context,
        modals=modals,
    )


@staff_member_required
def manage_type_versions(request, version_manager_id):
    """View that allows type versions management.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    try:
        # get the version manager
        version_manager = type_version_manager_api.get_by_id(
            version_manager_id, request=request
        )
        context = get_context_manage_template_versions(version_manager, "Type")

        # updating context regarding the installed apps
        # default back_url initialization
        context.update({"back_url": "core-admin:core_composer_app_types"})
        if "core_parser_app" in settings.INSTALLED_APPS:
            context.update(
                {"module_url": "core-admin:core_composer_app_type_modules"}
            )
        if "core_dashboard_app" in settings.INSTALLED_APPS:
            # the dashboard exposes the user's version managers
            # in this view, we come from the dashboard
            if version_manager.user:
                context.update({"back_url": "core-admin:core_dashboard_types"})

        assets = {
            "js": [
                {
                    "path": "core_main_app/common/js/templates/versions/set_current.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/restore.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/modals/disable.js",
                    "is_raw": False,
                },
            ]
        }

        modals = ["core_main_app/admin/templates/versions/modals/disable.html"]

        return admin_render(
            request,
            "core_composer_app/admin/types/versions.html",
            assets=assets,
            modals=modals,
            context=context,
        )
    except Exception as exception:
        return admin_render(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": str(exception)},
        )


@staff_member_required
def upload_type(request):
    """Upload type.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/upload/dependencies.js",
                "is_raw": False,
            },
            {
                "path": "core_composer_app/admin/js/types/upload/dependencies.js",
                "is_raw": False,
            },
            {
                "path": "core_composer_app/admin/js/types/upload/dependency_resolver.js",
                "is_raw": False,
            },
            {
                "path": "core_composer_app/admin/js/types/upload/dependencies.raw.js",
                "is_raw": True,
            },
        ]
    }

    context = {
        "object_name": "Type",
        "url": reverse("core-admin:core_composer_app_upload_type"),
        "redirect_url": reverse("core-admin:core_composer_app_types"),
    }

    # method is POST
    if request.method == "POST":
        form = UploadTypeForm(request.POST, request.FILES)
        context["upload_form"] = form

        if form.is_valid():
            return _save_type(request, assets, context)

        # Display error from the form
        return _upload_type_response(request, assets, context)

    # method is GET
    # render the form to upload a template
    context["upload_form"] = UploadTypeForm()
    return _upload_type_response(request, assets, context)


def _save_type(request, assets, context):
    """Save a type.

    Args:
        request:
        assets:
        context:

    Returns:

    """

    try:
        # get the schema name
        name = request.POST["name"]
        # get the file from the form
        xsd_file = request.FILES["xsd_file"]
        # read the content of the file
        xsd_data = read_xsd_file(xsd_file)
        # get the buckets
        buckets = request.POST.getlist("buckets")

        type_object = Type(filename=xsd_file.name, content=xsd_data)
        type_version_manager = TypeVersionManager(title=name)
        type_version_manager_api.insert(
            type_version_manager,
            type_object,
            request=request,
            list_bucket_ids=buckets,
        )
        return HttpResponseRedirect(
            reverse("core-admin:core_composer_app_types")
        )
    except exceptions.XSDError as xsd_error:
        return _handle_xsd_errors(
            request, assets, context, xsd_error, xsd_data, xsd_file.name
        )
    except exceptions.NotUniqueError:
        context[
            "errors"
        ] = "A type with the same name already exists. Please choose another name."
        return _upload_type_response(request, assets, context)
    except Exception as exception:
        context["errors"] = html_escape(str(exception))
        return _upload_type_response(request, assets, context)


def _handle_xsd_errors(
    request, assets, context, xsd_error, xsd_content, filename
):
    """Handle XSD errors. Builds dependency resolver if needed.

    Args:
        request:
        context:
        xsd_error:
        xsd_content:
        filename:

    Returns:

    """
    imports, includes = get_imports_and_includes(xsd_content)
    # a problem with includes/imports has been detected
    if len(includes) > 0 or len(imports) > 0:
        # build dependency resolver
        context["dependency_resolver"] = _get_dependency_resolver_html(
            imports, includes, xsd_content, filename, request=request
        )
        return _upload_type_response(request, assets, context)

    context["errors"] = html_escape(str(xsd_error))
    return _upload_type_response(request, assets, context)


def _get_dependency_resolver_html(
    imports, includes, xsd_data, filename, request
):
    """Return HTML for dependency resolver form.

    Args:
        imports:
        includes:
        xsd_data:
        filename:
        request:

    Returns:

    """
    # build the list of dependencies
    current_types = type_version_manager_api.get_global_version_managers(
        request=request
    )
    list_dependencies_template = loader.get_template(
        "core_main_app/admin/list_dependencies.html"
    )
    context = {
        "templates": [
            template for template in current_types if not template.is_disabled
        ]
    }
    list_dependencies_html = list_dependencies_template.render(context)

    # build the dependency resolver form
    dependency_resolver_template = loader.get_template(
        "core_main_app/admin/dependency_resolver.html"
    )
    context = {
        "imports": imports,
        "includes": includes,
        "xsd_content": html_escape(xsd_data),
        "filename": filename,
        "dependencies": list_dependencies_html,
    }
    return dependency_resolver_template.render(context)


def _upload_type_response(request, assets, context):
    """Render type upload response.

    Args:
        request:
        context:

    Returns:

    """
    return admin_render(
        request,
        "core_composer_app/admin/types/upload.html",
        assets=assets,
        context=context,
    )


@staff_member_required
def upload_type_version(request, version_manager_id):
    """Upload type version.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/upload/dependencies.js",
                "is_raw": False,
            },
            {
                "path": "core_composer_app/admin/js/types/upload/dependencies.js",
                "is_raw": False,
            },
            {
                "path": "core_composer_app/admin/js/types/upload/dependency_resolver.js",
                "is_raw": False,
            },
            {
                "path": "core_composer_app/admin/js/types/upload/dependencies.raw.js",
                "is_raw": True,
            },
        ]
    }

    type_version_manager = type_version_manager_api.get_by_id(
        version_manager_id, request=request
    )
    context = {
        "object_name": "Type",
        "version_manager": type_version_manager,
        "url": reverse(
            "core-admin:core_composer_app_upload_type_version",
            kwargs={"version_manager_id": type_version_manager.id},
        ),
        "redirect_url": reverse(
            "core-admin:core_composer_app_manage_type_versions",
            kwargs={"version_manager_id": type_version_manager.id},
        ),
    }

    # method is POST
    if request.method == "POST":
        form = UploadVersionForm(request.POST, request.FILES)
        context["upload_form"] = form

        if form.is_valid():
            return _save_type_version(
                request, assets, context, type_version_manager
            )

        # Display errors from the form
        return _upload_type_response(request, assets, context)

    # method is GET
    # render the form to upload a template
    context["upload_form"] = UploadVersionForm()
    return _upload_type_response(request, assets, context)


def _save_type_version(request, assets, context, type_version_manager):
    """Save a type version.

    Args:
        request:
        assets:
        context:
        type_version_manager:

    Returns:

    """
    # get the file from the form
    xsd_file = request.FILES["xsd_file"]
    # read the content of the file
    xsd_data = read_xsd_file(xsd_file)

    try:
        type_object = Type(filename=xsd_file.name, content=xsd_data)
        type_version_manager_api.insert(
            type_version_manager, type_object, request=request
        )
        return HttpResponseRedirect(
            reverse(
                "core-admin:core_composer_app_manage_type_versions",
                kwargs={"version_manager_id": str(type_version_manager.id)},
            )
        )
    except exceptions.XSDError as xsd_error:
        return _handle_xsd_errors(
            request, assets, context, xsd_error, xsd_data, xsd_file.name
        )
    except Exception as exception:
        context["errors"] = html_escape(str(exception))
        return _upload_type_response(request, assets, context)


@staff_member_required
def manage_buckets(request):
    """Manage buckets view.

    Args:
        request:

    Returns:

    """

    context = {"object_name": "Bucket", "buckets": bucket_api.get_all()}

    assets = {
        "js": [
            {"path": "core_composer_app/admin/js/bucket.js", "is_raw": False},
            {
                "path": "core_composer_app/admin/js/bucket.raw.js",
                "is_raw": True,
            },
            {
                "path": "core_main_app/common/js/backtoprevious.js",
                "is_raw": True,
            },
            EditBucketView.get_modal_js_path(),
        ],
        "css": ["core_composer_app/common/css/bucket.css"],
    }

    modals = [
        "core_composer_app/admin/buckets/modals/delete.html",
        EditBucketView.get_modal_html_path(),
    ]

    return admin_render(
        request,
        "core_composer_app/admin/buckets/list.html",
        assets=assets,
        modals=modals,
        context=context,
    )


@staff_member_required
def upload_bucket(request):
    """Upload bucket.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/common/js/backtoprevious.js",
                "is_raw": True,
            }
        ]
    }

    context = {"object_name": "Bucket"}
    if request.method == "POST":
        form = BucketForm(request.POST)
        if form.is_valid():
            bucket_label = request.POST["label"]
            bucket = Bucket(label=bucket_label)
            try:
                bucket_api.upsert(bucket)
                return redirect(
                    reverse("core-admin:core_composer_app_buckets")
                )
            except NotUniqueError:
                context[
                    "errors"
                ] = "A bucket with the same name already exists."
            except Exception as exception:
                context["errors"] = str(exception)

    else:
        form = BucketForm()

    context["form"] = form
    return admin_render(
        request,
        "core_composer_app/admin/buckets/add.html",
        context=context,
        assets=assets,
    )


@staff_member_required
def manage_type_buckets(request, version_manager_id):
    """Manage buckets of a type.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    # get the version manager
    version_manager = None

    try:
        version_manager = type_version_manager_api.get_by_id(
            version_manager_id, request=request
        )
    except ModelError as exception:
        logger.error(
            "manage_type_buckets threw a ModelError: %s", str(exception)
        )
        return admin_render(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": str(exception)},
        )
    except DoesNotExist as exception:
        # TODO: catch exception, redirect to error page
        logger.warning(
            "manage_type_buckets threw a DoesNotExist exception: %s",
            str(exception),
        )

    context = {
        "version_manager": version_manager,
        "buckets": bucket_api.get_all(),
    }

    assets = {
        "css": ["core_composer_app/common/css/bucket.css"],
        "js": [
            {
                "path": "core_main_app/common/js/backtoprevious.js",
                "is_raw": True,
            }
        ],
    }
    if request.method == "POST":
        form = EditTypeBucketsForm(request.POST)
        if form.is_valid():
            buckets = request.POST.getlist("buckets")
            bucket_api.update_type_buckets(version_manager, buckets)
            return redirect(reverse("core-admin:core_composer_app_types"))
    else:
        form = EditTypeBucketsForm()

    context["form"] = form
    return admin_render(
        request,
        "core_composer_app/admin/buckets/edit.html",
        assets=assets,
        context=context,
    )
