"""Composer AJAX admin views
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils.html import escape

from core_main_app.commons import exceptions
from core_main_app.components.template.api import (
    init_template_with_dependencies,
)
from core_main_app.views.admin.ajax import (
    _get_xsd_content_from_html,
    _get_dependencies_dict,
)
from core_main_app.views.common.ajax import EditObjectModalView
from core_composer_app.components.bucket import api as bucket_api
from core_composer_app.components.bucket.models import Bucket
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager import (
    api as type_version_manager_api,
)
from core_composer_app.components.type_version_manager.models import (
    TypeVersionManager,
)
from core_composer_app.views.admin.forms import EditBucketForm


@staff_member_required
def delete_bucket(request):
    """Delete a bucket.

    Args:
        request:

    Returns:

    """
    try:
        bucket_id = request.POST["bucket_id"]

        bucket = bucket_api.get_by_id(bucket_id)
        bucket_api.delete(bucket)
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@staff_member_required
def resolve_dependencies(request):
    """Resolve import/includes to avoid local references.

    Args:
        request:

    Returns:

    """
    try:
        # Get the parameters
        name = request.POST.get("name", None)
        version_manager_id = request.POST.get("version_manager_id", "")
        filename = request.POST["filename"]
        xsd_content = request.POST["xsd_content"]
        schema_locations = request.POST.getlist("schemaLocations[]")
        dependencies = request.POST.getlist("dependencies[]")
        buckets = request.POST.getlist("buckets[]")

        # create new object
        type_object = Type(
            filename=filename, content=_get_xsd_content_from_html(xsd_content)
        )
        init_template_with_dependencies(
            type_object,
            _get_dependencies_dict(schema_locations, dependencies),
            request=request,
        )

        # get the version manager or create a new one
        if version_manager_id != "":
            type_version_manager = type_version_manager_api.get_by_id(
                version_manager_id, request=request
            )
        else:
            type_version_manager = TypeVersionManager(title=name)
        type_version_manager_api.insert(
            type_version_manager,
            type_object,
            request=request,
            list_bucket_ids=buckets,
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")


class EditBucketView(EditObjectModalView):
    """Edit Bucket View"""

    form_class = EditBucketForm
    model = Bucket
    success_url = reverse_lazy("core-admin:core_composer_app_buckets")
    success_message = "Label edited."

    def _save(self, form):
        """_save

        Args:
            form

        Returns:
        """
        # Save treatment.
        try:
            self.object.label = form.cleaned_data.get("label")
            bucket_api.upsert(self.object)
        except exceptions.NotUniqueError:
            form.add_error(
                None,
                "A bucket with the same label already exists. Please choose another label.",
            )
        except Exception as exception:
            form.add_error(None, str(exception))
