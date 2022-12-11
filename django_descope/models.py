import logging

from descope import REFRESH_SESSION_TOKEN_NAME, SESSION_TOKEN_NAME, DescopeClient
from django.contrib.auth import models as auth_models
from django.core.cache import cache
from django.utils.functional import cached_property

from .settings import PROJECT_ID

logger = logging.getLogger(__name__)


class DescopeUser(auth_models.User):
    class Meta:
        proxy = True

    # User is always active since Descioe will never issue a token for an
    # inactive user
    is_active = True
    _descope = DescopeClient(PROJECT_ID)

    def sync(self, token, refresh_token):
        self.token = token
        self.access = token.get(SESSION_TOKEN_NAME).get("jwt")
        self.refresh = token.get(REFRESH_SESSION_TOKEN_NAME, {}).get(
            "jwt", refresh_token
        )
        self.user = token.get("user")
        self.firstSeen = token.get("firstSeen")
        self.username = self._me.get("userId")
        self.email = self._me.get("email")
        self.is_staff = "is_staff" in self._roles
        self.is_superuser = "is_superuser" in self._roles
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
