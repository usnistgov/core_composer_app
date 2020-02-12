=================
Core Composer App
=================

Template and type composer for the curator core project.

Quick start
===========

1. Add "core_composer_app" to your INSTALLED_APPS setting
---------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_composer_app',
    ]

2. Include the core_composer_app URLconf in your project urls.py
----------------------------------------------------------------

.. code:: python

    url(r'^composer/', include('core_composer_app.urls')),
