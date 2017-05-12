"""Url router for the REST API
"""
from django.conf.urls import url
from core_main_app.rest.template import views as template_views
from core_composer_app.rest.type_version_manager import views as type_version_manager_views
from core_composer_app.rest.type import views as type_views


urlpatterns = [
    url(r'^type/download', template_views.download,
        name='core_main_app_rest_type_download'),

    url(r'^type-version-manager/get/all/global$', type_version_manager_views.get_all_globals,
        name='core_main_app_rest_type_version_manager_get_all_globals'),

    url(r'^type-version-manager/get/all/user$', type_version_manager_views.get_by_user,
        name='core_main_app_rest_type_version_manager_get_all_by_user'),
    #
    url(r'^type-version-manager/get$', type_version_manager_views.get_by_id,
        name='core_main_app_rest_type_version_manager_get'),

    url(r'^type/get', type_views.get_by_id,
        name='core_main_app_rest_type_get_by_id'),

    url(r'^type', type_views.type,
        name='core_main_app_rest_type'),

]
