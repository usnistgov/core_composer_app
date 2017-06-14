# core_composer_app

core_composer_app is a Django app.

# Quick start

1. Add "core_composer_app" to your INSTALLED_APPS setting like this:

  ```python
  INSTALLED_APPS = [
      ...
      'core_composer_app',
  ]
  ```

  2. Include the core_dashboard_app URLconf in your project urls.py like this::

  ```python
  url(r'^composer/', include('core_composer_app.urls')),
  ```

