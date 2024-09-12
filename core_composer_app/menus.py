""" Add Composer in main menu
"""

from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Composer", reverse("core_composer_index")))


types_children = (
    MenuItem(
        "Type List", reverse("core-admin:core_composer_app_types"), icon="list"
    ),
    MenuItem(
        "Upload New Type",
        reverse("core-admin:core_composer_app_upload_type"),
        icon="upload",
    ),
    MenuItem(
        "Manage Buckets",
        reverse("core-admin:core_composer_app_buckets"),
        icon="tags",
    ),
)

Menu.add_item("admin", MenuItem("TYPES", None, children=types_children))
