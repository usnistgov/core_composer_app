"""Core Composer App Settings
"""

from django.conf import settings

if not settings.configured:
    settings.configure()
