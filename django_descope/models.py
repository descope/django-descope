import logging

from descope import SESSION_TOKEN_NAME
from django.contrib import auth
from django.core.cache import cache

from . import descope_client
from .settings import IS_STAFF_ROLE, IS_SUPERUSER_ROLE

logger = logging.getLogger(__name__)


class DescopeUser(auth.get_user_model()):
    class Meta:
        proxy = True

    # User is always active since Descope will never issue a token for an
    # inactive user
    is_active = True

    def sync(self, session, refresh):
        self.session_token = session[SESSION_TOKEN_NAME]  # this should always exist
        self.refresh_token = refresh
        self.username = self._me.get("userId")
        self.user = self.username
        self.email = self._me.get("email")
        self.is_staff = descope_client.validate_roles(
            self.session_token, [IS_STAFF_ROLE]
        )
        self.is_superuser = descope_client.validate_roles(
            self.session_token, [IS_SUPERUSER_ROLE]
        )
        self.save()

    def __str__(self):
        return f"DescopeUser {self.username}"

    @property
    def _me(self):
        return cache.get_or_set(
            f"descope_me:{self.username}", lambda: descope_client.me(self.refresh_token)
        )

    def get_username(self):
        return self.username
