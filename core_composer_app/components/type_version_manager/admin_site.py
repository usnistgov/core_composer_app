""" Custom admin site for the Type Version Manager model
"""
from django.contrib import admin


class CustomTypeVersionManagerAdmin(admin.ModelAdmin):
    """CustomTypeVersionManagerAdmin"""

    exclude = ["_cls"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Type Version Managers"""
        return False
