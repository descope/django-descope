from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

WEB_COMPONENT_SRC = getattr(
    settings, "DESCOPE_WEB_COMPONENT_SRC", "https://unpkg.com/@descope/web-component"
)

PROJECT_ID = getattr(settings, "DESCOPE_PROJECT_ID", None)
if not PROJECT_ID:
    raise ImproperlyConfigured('"DESCOPE_PROJECT_ID" is required!')

# Role names to create in Descope that will map to User attributes
IS_STAFF_ROLE = getattr(settings, "DESCOPE_IS_STAFF_ROLE", "is_staff")
IS_SUPERUSER_ROLE = getattr(settings, "DESCOPE_IS_SUPERUSER_ROLE", "is_superuser")
