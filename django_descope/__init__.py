from descope import DescopeClient

from django_descope.conf import settings

descope_client = DescopeClient(
    project_id=settings.DESCOPE_PROJECT_ID,
    management_key=settings.DESCOPE_MANAGEMENT_KEY,
)

all = [descope_client]
