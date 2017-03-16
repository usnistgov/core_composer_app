"""Composer app user views
"""
from django.contrib.staticfiles import finders
from django.http.response import HttpResponse
from django.core.servers.basehttp import FileWrapper
from os.path import join
from cStringIO import StringIO

from core_main_app.utils.xml import xsl_transform
from core_main_app.utils.rendering import render
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_composer_app.components.type_version_manager import api as type_version_manager_api
from core_composer_app.components.bucket import api as bucket_api

from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE
from xml_utils.xsd_tree.operations.annotation import remove_annotations
from xml_utils.xsd_tree.xsd_tree import XSDTree
from xml_utils.xsd_types.xsd_types import get_xsd_types

# FIXME: add permissions
# TODO: see if sessions are problematic


def index(request):
    """ Page that allows to select a template to start composing

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [],
        "css": ['core_curate_app/user/css/style.css']
    }

    global_active_template_list = template_version_manager_api.get_active_global_version_manager()
    user_active_template_list = template_version_manager_api.get_active_version_manager_by_user_id(request.user.id)

    # Add new template option to global templates
    global_active_template_list.insert(0, {
        'title': 'New Template',
        'current': 'new'
    })

    context = {
        'global_templates': global_active_template_list,
        'user_templates': user_active_template_list,
    }

    return render(request,
                  'core_composer_app/user/index.html',
                  assets=assets,
                  context=context)


def build_template(request, template_id):
    """View that allows to build the Template

    Args:
        request:
        template_id:

    Returns:

    """
    if template_id == "new":
        base_template_path = finders.find(join('core_composer_app', 'user', 'xsd', 'new_base_template.xsd'))
        xsd_string = _read_file_content(base_template_path)
    else:
        template = template_api.get(template_id)
        xsd_string = template.content

    request.session['newXmlTemplateCompose'] = xsd_string
    request.session['includedTypesCompose'] = []

    # store the current includes/imports
    xsd_tree = XSDTree.build_tree(xsd_string)
    includes = xsd_tree.findall("{}include".format(LXML_SCHEMA_NAMESPACE))
    for el_include in includes:
        if 'schemaLocation' in el_include.attrib:
            request.session['includedTypesCompose'].append(el_include.attrib['schemaLocation'])
    imports = xsd_tree.findall("{}import".format(LXML_SCHEMA_NAMESPACE))
    for el_import in imports:
        if 'schemaLocation' in el_import.attrib:
            request.session['includedTypesCompose'].append(el_import.attrib['schemaLocation'])

    # remove annotations from the tree
    remove_annotations(xsd_tree)
    xsd_string = XSDTree.tostring(xsd_tree)

    # loads XSLT
    xslt_path = finders.find(join('core_composer_app', 'user', 'xsl', 'xsd2html.xsl'))
    # reads XSLT
    xslt_string = _read_file_content(xslt_path)
    # transform XML to HTML
    xsd_to_html_string = xsl_transform(xsd_string, xslt_string)

    # 1) Get user defined types
    user_types = type_version_manager_api.get_version_managers_by_user(str(request.user.id))
    # 2) Get buckets
    buckets = bucket_api.get_all()

    # 3) no_buckets_types: list of types that are not assigned to a specific bucket
    no_buckets_types = type_version_manager_api.get_no_buckets_types()

    # 4) Build list of built-in types
    built_in_types = []
    for built_in_type in get_xsd_types():
        built_in_types.append({'current': 'built_in_type', 'title': built_in_type})

    assets = {
        "js": [
            {
                "path": 'core_composer_app/user/js/build_template.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/user/js/build_template.raw.js',
                "is_raw": True
            },
            {
                "path": 'core_composer_app/user/js/xpath.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/user/js/menus.js',
                "is_raw": False
            },
            {
                "path": 'core_composer_app/user/js/xsd_tree.js',
                "is_raw": False
            },
        ],
        "css": ['core_main_app/common/css/XMLTree.css',
                'core_composer_app/common/css/bucket.css',
                'core_composer_app/user/css/menu.css',
                'core_composer_app/user/css/style.css',
                'core_composer_app/user/css/xsd_tree.css']
    }
    context = {
        'buckets': buckets,
        'built_in_types': built_in_types,
        'no_buckets_types': no_buckets_types,
        'user_types': user_types,
        'xsd_form': xsd_to_html_string,
        'template_id': template_id,
    }

    modals = [
        'core_composer_app/user/builder/menus/sequence.html',
        'core_composer_app/user/builder/menus/element.html',
        'core_composer_app/user/builder/menus/element_root.html',

        'core_composer_app/user/builder/modals/root_type_name.html',
        'core_composer_app/user/builder/modals/element_name.html',
        'core_composer_app/user/builder/modals/insert_element.html',
        'core_composer_app/user/builder/modals/delete_element.html',
        'core_composer_app/user/builder/modals/change_type.html',
        'core_composer_app/user/builder/modals/save_template.html',
        'core_composer_app/user/builder/modals/save_type.html',
        'core_composer_app/user/builder/modals/save_success.html',
        'core_composer_app/user/builder/modals/occurrences.html',
        'core_composer_app/user/builder/modals/errors.html',
    ]

    return render(request,
                  'core_composer_app/user/build_template.html',
                  assets=assets,
                  context=context,
                  modals=modals)


def download_xsd(request):
    """Makes the current XSD available for download.

    Args:
        request:

    Returns:

    """
    xsd_string = request.session['newXmlTemplateCompose']

    # build a file
    # TODO: test encoding
    template_file = StringIO(xsd_string.encode('utf-8'))

    # build response with file
    response = HttpResponse(FileWrapper(template_file), content_type='application/xsd')
    response['Content-Disposition'] = 'attachment; filename=schema.xsd'

    return response


# FIXME: refactor
def _read_file_content(file_path):
    """Reads the content of a file

    Args:
        file_path:

    Returns:

    """
    with open(file_path) as _file:
        file_content = _file.read()
        return file_content
