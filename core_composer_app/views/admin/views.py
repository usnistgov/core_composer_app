"""Composer admin views
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.html import escape as html_escape
from django.template import loader
from django.template.context import Context

from core_composer_app.components.bucket.models import Bucket
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager import api as type_version_manager_api
from core_composer_app.components.bucket import api as bucket_api
from core_composer_app.components.type_version_manager.models import TypeVersionManager
from core_composer_app.views.admin.forms import BucketForm, UploadTypeForm, EditTypeBucketsForm

from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.rendering import admin_render
from core_main_app.settings import INSTALLED_APPS
from core_main_app.commons import exceptions
from core_main_app.utils.xml import get_imports_and_includes
from core_main_app.views.admin.forms import UploadVersionForm
from core_main_app.views.admin.views import _read_xsd_file


@staff_member_required
def manage_types(request):
    """View that allows type management

    Args:
        request:

    Returns:

    """
    # get all types
    type_version_managers = type_version_manager_api.get_global_version_managers()
    # get buckets
    buckets = bucket_api.get_all()

    context = {
        'object_name': "Type",
        'available': [type_version_manager for type_version_manager in type_version_managers
                      if not type_version_manager.is_disabled],
        'disabled': [type_version_manager for type_version_manager in type_version_managers
                     if type_version_manager.is_disabled],
        'buckets': buckets
    }

    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/templates/list/restore.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/admin/js/templates/list/modals/edit.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/admin/js/templates/list/modals/disable.js',
                "is_raw": False
            }
        ],
        "css": ['core_composer_app/common/css/bucket.css']
    }

    modals = [
        "core_main_app/admin/templates/list/modals/edit.html",
        "core_main_app/admin/templates/list/modals/disable.html"
    ]

    return admin_render(request,
                        'core_composer_app/admin/types/list.html',
                        assets=assets,
                        context=context,
                        modals=modals)


@staff_member_required
def manage_type_versions(request, version_manager_id):
    """View that allows type versions management

    Args:
        request:
        version_manager_id:

    Returns:

    """
    # get the version manager
    version_manager = None

    try:
        version_manager = version_manager_api.get(version_manager_id)
    except:
        # TODO: catch good exception, redirect to error page
        pass

    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/templates/versions/set_current.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/admin/js/templates/versions/restore.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/admin/js/templates/versions/modals/disable.js',
                "is_raw": False
            }
        ]
    }

    modals = [
        "core_main_app/admin/templates/versions/modals/disable.html"
    ]

    # Use categorized version for easier manipulation in template
    versions = version_manager.versions
    categorized_versions = {
        "available": [],
        "disabled": []
    }

    for index, version in enumerate(versions, 1):
        indexed_version = {
            "index": index,
            "object": version
        }

        if version not in version_manager.disabled_versions:
            categorized_versions["available"].append(indexed_version)
        else:
            categorized_versions["disabled"].append(indexed_version)

    version_manager.versions = categorized_versions

    context = {
        'object_name': 'Type',
        "version_manager": version_manager
    }

    # FIXME: make this more dynamic?
    if 'core_parser_app' in INSTALLED_APPS:
        context["core_parser_app_installed"] = True

    return admin_render(request,
                        'core_composer_app/admin/types/versions.html',
                        assets=assets,
                        modals=modals,
                        context=context)


@staff_member_required
def upload_type(request):
    """Upload type

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/templates/upload/dependencies.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/types/upload/dependencies.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/types/upload/dependency_resolver.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/types/upload/dependencies.raw.js',
                "is_raw": True
            }
        ]
    }

    context = {
        'object_name': "Type",
        'url': reverse("admin:core_composer_app_upload_type"),
        'redirect_url': reverse("admin:core_composer_app_types")
    }

    # method is POST
    if request.method == 'POST':
        form = UploadTypeForm(request.POST, request.FILES)
        context['upload_form'] = form

        if form.is_valid():
            return _save_type(request, assets, context)
        else:
            # Display error from the form
            return _upload_type_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context['upload_form'] = UploadTypeForm()
        return _upload_type_response(request, assets, context)


def _save_type(request, assets, context):
    """Saves a type

    Args:
        request:
        assets:
        context:

    Returns:

    """
    # get the schema name
    name = request.POST['name']
    # get the file from the form
    xsd_file = request.FILES['xsd_file']
    # read the content of the file
    xsd_data = _read_xsd_file(xsd_file)
    # get the buckets
    buckets = request.POST.getlist('buckets')

    try:
        type_object = Type(filename=xsd_file.name, content=xsd_data)
        type_version_manager = TypeVersionManager(title=name)
        type_version_manager_api.insert(type_version_manager, type_object, buckets)
        return HttpResponseRedirect(reverse("admin:core_composer_app_types"))
    except exceptions.XSDError, xsd_error:
        return _handle_xsd_errors(request, assets, context, xsd_error, xsd_data, xsd_file.name)
    except Exception, e:
        context['errors'] = html_escape(e.message)
        return _upload_type_response(request, assets, context)


def _handle_xsd_errors(request, assets, context, xsd_error, xsd_content, filename):
    """Handles XSD errors. Builds dependency resolver if needed.

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
        context['dependency_resolver'] = _get_dependency_resolver_html(imports, includes, xsd_content,
                                                                       filename)
        return _upload_type_response(request, assets, context)
    else:
        context['errors'] = html_escape(xsd_error.message)
        return _upload_type_response(request, assets, context)


def _get_dependency_resolver_html(imports, includes, xsd_data, filename):
    """
    Return HTML for dependency resolver form
    :param imports:
    :param includes:
    :param xsd_data:
    :return:
    """
    # build the list of dependencies
    current_types = type_version_manager_api.get_global_version_managers()
    list_dependencies_template = loader.get_template('core_main_app/admin/list_dependencies.html')
    context = Context({
        'templates': [template for template in current_types if not template.is_disabled],
    })
    list_dependencies_html = list_dependencies_template.render(context)

    # build the dependency resolver form
    dependency_resolver_template = loader.get_template('core_main_app/admin/dependency_resolver.html')
    context = Context({
        'imports': imports,
        'includes': includes,
        'xsd_content': html_escape(xsd_data),
        'filename': filename,
        'dependencies': list_dependencies_html,
    })
    return dependency_resolver_template.render(context)


def _upload_type_response(request, assets, context):
    """Renders type upload response

    Args:
        request:
        context:

    Returns:

    """
    return admin_render(request,
                        'core_composer_app/admin/types/upload.html',
                        assets=assets,
                        context=context)


@staff_member_required
def upload_type_version(request, version_manager_id):
    """Upload type version

    Args:
        request:
        version_manager_id:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/templates/upload/dependencies.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/types/upload/dependencies.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/types/upload/dependency_resolver.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/types/upload/dependencies.raw.js',
                "is_raw": True
            }
        ]
    }

    type_version_manager = version_manager_api.get(version_manager_id)
    context = {
        'object_name': "Type",
        'version_manager': type_version_manager,
        'url': reverse("admin:core_composer_app_upload_type_version",
                       kwargs={'version_manager_id': type_version_manager.id}),
        'redirect_url': reverse("admin:core_composer_app_manage_type_versions",
                                kwargs={'version_manager_id': type_version_manager.id})
    }

    # method is POST
    if request.method == 'POST':
        form = UploadVersionForm(request.POST,  request.FILES)
        context['upload_form'] = form

        if form.is_valid():
            return _save_type_version(request, assets, context, type_version_manager)
        else:
            # Display errors from the form
            return _upload_type_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context['upload_form'] = UploadVersionForm()
        return _upload_type_response(request, assets, context)


def _save_type_version(request, assets, context, type_version_manager):
    """Saves a type version

    Args:
        request:
        assets:
        context:
        type_version_manager:

    Returns:

    """
    # get the file from the form
    xsd_file = request.FILES['xsd_file']
    # read the content of the file
    xsd_data = _read_xsd_file(xsd_file)

    try:
        type_object = Type(filename=xsd_file.name, content=xsd_data)
        type_version_manager_api.insert(type_version_manager, type_object)
        return HttpResponseRedirect(reverse("admin:core_composer_app_manage_type_versions",
                                            kwargs={'version_manager_id': str(type_version_manager.id)}))
    except exceptions.XSDError, xsd_error:
        return _handle_xsd_errors(request, assets, context, xsd_error, xsd_data, xsd_file.name)
    except Exception, e:
        context['errors'] = html_escape(e.message)
        return _upload_type_response(request, assets, context)


@staff_member_required
def manage_buckets(request):
    """Manage buckets view

    Args:
        request:

    Returns:

    """

    context = {
        'object_name': "Bucket",
        'buckets': bucket_api.get_all()
    }

    assets = {
        "js": [
            {
                "path": 'core_composer_app/admin/js/bucket.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/admin/js/bucket.raw.js',
                "is_raw": True
            },
        ],
        "css": ['core_composer_app/common/css/bucket.css']
    }

    return admin_render(request,
                        'core_composer_app/admin/buckets/list.html',
                        assets=assets,
                        modals=[],
                        context=context)


@staff_member_required
def upload_bucket(request):
    """Upload bucket

    Args:
        request:

    Returns:

    """
    context = {
        'object_name': 'Bucket'
    }
    if request.method == 'POST':
        form = BucketForm(request.POST)
        if form.is_valid():
            bucket_label = request.POST['label']
            bucket = Bucket(label=bucket_label)
            try:
                bucket_api.upsert(bucket)
                return redirect(reverse('admin:core_composer_app_buckets'))
            except Exception, e:
                context['errors'] = e.message

    else:
        form = BucketForm()

    context['form'] = form
    return admin_render(request,
                        'core_composer_app/admin/buckets/add.html',
                        context=context)


@staff_member_required
def manage_type_buckets(request, version_manager_id):
    """

    Args:
        request:
        version_manager_id:

    Returns:

    """
    # get the version manager
    version_manager = None

    try:
        version_manager = version_manager_api.get(version_manager_id)
    except:
        # TODO: catch good exception, redirect to error page
        pass

    context = {
        'version_manager': version_manager,
        'buckets': bucket_api.get_all()
    }

    assets = {
        "css": ['core_composer_app/common/css/bucket.css']
    }
    if request.method == 'POST':
        form = EditTypeBucketsForm(request.POST)
        if form.is_valid():
            buckets = request.POST.getlist('buckets')
            bucket_api.update_type_buckets(version_manager, buckets)
            return redirect(reverse('admin:core_composer_app_types'))
    else:
        form = EditTypeBucketsForm()

    context['form'] = form
    return admin_render(request,
                        'core_composer_app/admin/edit_buckets.html',
                        assets=assets,
                        context=context)
