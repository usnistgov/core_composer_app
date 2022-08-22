"""Url router for the administration site
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path, reverse_lazy

from core_main_app.admin import core_admin_site

from core_composer_app.components.bucket.models import Bucket
from core_composer_app.components.type.admin_site import CustomTypeAdmin
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager.admin_site import (
    CustomTypeVersionManagerAdmin,
)
from core_composer_app.components.type_version_manager.models import TypeVersionManager
from core_composer_app.views.admin import views as admin_views, ajax as admin_ajax
from core_composer_app.views.admin.ajax import EditBucketView
from core_composer_app.views.user.ajax import EditTypeVersionManagerView


parser_url = []
if "core_parser_app" in settings.INSTALLED_APPS:
    from core_parser_app.views.admin import views as admin_parser_views

    parser_url = [
        re_path(
            r"^type/modules/(?P<pk>\w+)",
            staff_member_required(
                admin_parser_views.ManageModulesAdminView.as_view(
                    back_to_previous_url="core-admin:core_composer_app_manage_type_versions"
                )
            ),
            name="core_composer_app_type_modules",
        ),
    ]

admin_urls = [
    re_path(r"^types$", admin_views.manage_types, name="core_composer_app_types"),
    re_path(
        r"^type/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(
            EditTypeVersionManagerView.as_view(
                success_url=reverse_lazy("core-admin:core_composer_app_types")
            )
        ),
        name="core_composer_app_edit_type",
    ),
    re_path(
        r"^type/upload$", admin_views.upload_type, name="core_composer_app_upload_type"
    ),
    re_path(
        r"^type/upload/(?P<version_manager_id>\w+)",
        admin_views.upload_type_version,
        name="core_composer_app_upload_type_version",
    ),
    re_path(
        r"^type/versions/(?P<version_manager_id>\w+)",
        admin_views.manage_type_versions,
        name="core_composer_app_manage_type_versions",
    ),
    re_path(
        r"^type/buckets/(?P<version_manager_id>\w+)",
        admin_views.manage_type_buckets,
        name="core_composer_app_type_buckets",
    ),
    re_path(r"^buckets$", admin_views.manage_buckets, name="core_composer_app_buckets"),
    re_path(
        r"^bucket/upload$",
        admin_views.upload_bucket,
        name="core_composer_app_upload_bucket",
    ),
    re_path(
        r"^bucket/delete$",
        admin_ajax.delete_bucket,
        name="core_composer_app_delete_bucket",
    ),
    re_path(
        r"^type/resolve-dependencies",
        admin_ajax.resolve_dependencies,
        name="core_composer_app_resolve_dependencies",
    ),
    re_path(
        r"^bucket/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(EditBucketView.as_view()),
        name="core_composer_app_edit_bucket",
    ),
]

admin.site.register(Bucket)
admin.site.register(Type, CustomTypeAdmin)
admin.site.register(TypeVersionManager, CustomTypeVersionManagerAdmin)

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: parser_url + admin_urls + urls
