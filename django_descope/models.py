import logging

from descope import DescopeClient
from django.contrib.auth import models as auth_models
from django.core.cache import cache
from django.utils.functional import cached_property

from .settings import IS_STAFF_ROLE, IS_SUPERUSER_ROLE, PROJECT_ID

logger = logging.getLogger(__name__)


class DescopeUser(auth_models.User):
    class Meta:
        proxy = True

    # User is always active since Descioe will never issue a token for an
    # inactive user
    is_active = True
    _descope = DescopeClient(PROJECT_ID)

    def sync(self, session, refresh):
        self.token = session
        self.session = session.get("jwt")
        self.refresh = refresh
        self.user = session.get("user")
        self.firstSeen = session.get("firstSeen")
        self.username = self._me.get("userId")
        self.email = self._me.get("email")
        self.is_staff = IS_STAFF_ROLE in self._roles
        self.is_superuser = IS_SUPERUSER_ROLE in self._roles
        self.save()

    def __str__(self):
        return f"DescopeUser {self.username}"

    @cached_property
    def _me(self):
        return cache.get_or_set(
            f"descope_me:{self.username}", lambda: self._descope.me(self.refresh)
        )

    @cached_property
    def _roles(self):
        return self.token.get("roles", [])

    def get_username(self):
        return self.username
