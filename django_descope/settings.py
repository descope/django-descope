from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# renovate depName=@descope/web-component datasource=npm
WEB_COMPONENT_VERSION = getattr(settings, "DESCOPE_WEB_COMPONENT_VERSION", "3.23.1")
WEB_COMPONENT_SRC = getattr(
    settings,
    "DESCOPE_WEB_COMPONENT_SRC",
    "https://unpkg.com/@descope/web-component@{:s}/dist/index.js".format(
        WEB_COMPONENT_VERSION
    ),
)

MANAGEMENT_KEY = getattr(settings, "DESCOPE_MANAGEMENT_KEY", "")
PROJECT_ID = getattr(settings, "DESCOPE_PROJECT_ID", "")
if not PROJECT_ID:
    raise ImproperlyConfigured('"DESCOPE_PROJECT_ID" is required!')

# Role names to create in Descope that will map to User attributes
IS_STAFF_ROLE = getattr(settings, "DESCOPE_IS_STAFF_ROLE", "is_staff")
IS_SUPERUSER_ROLE = getattr(settings, "DESCOPE_IS_SUPERUSER_ROLE", "is_superuser")
