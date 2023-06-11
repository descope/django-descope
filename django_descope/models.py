import logging

from descope import DescopeClient
from django.contrib.auth import models as auth_models
from django.core.cache import cache

from .settings import IS_STAFF_ROLE, IS_SUPERUSER_ROLE, MANAGEMENT_KEY, PROJECT_ID

logger = logging.getLogger(__name__)


class DescopeUser(auth_models.User):
    class Meta:
        proxy = True

    # User is always active since Descope will never issue a token for an
    # inactive user
    is_active = True
    descope = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

    def sync(self, session, refresh):
        self.session = session
        self.token = self.session["jwt"]
        self.refresh = refresh
        self.firstSeen = self.session.get("firstSeen")
        self.username = self._me.get("userId")
        self.user = self.username
        self.email = self._me.get("email")
        self.is_staff = self.descope.validate_roles(self.session, [IS_STAFF_ROLE])
        self.is_superuser = self.descope.validate_roles(
            self.session, [IS_SUPERUSER_ROLE]
        )
        self.save()

    def __str__(self):
        return f"DescopeUser {self.username}"

    @property
    def _me(self):
        return cache.get_or_set(
            f"descope_me:{self.username}", lambda: self.descope.me(self.refresh)
        )

    def get_username(self):
        return self.username
