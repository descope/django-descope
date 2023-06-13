from descope import DescopeClient

from .settings import MANAGEMENT_KEY, PROJECT_ID

descope_client = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

all = [descope_client]
