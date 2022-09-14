""" Custom admin site for the Type model
"""
from django.contrib import admin


class CustomTypeAdmin(admin.ModelAdmin):
    """CustomTypeAdmin"""

    readonly_fields = ["checksum", "hash", "file"]
    exclude = ["_cls"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Types"""
        return False
