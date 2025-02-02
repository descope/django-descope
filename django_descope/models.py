import logging

from descope import SESSION_TOKEN_NAME
from django.contrib import auth
from django.core.cache import cache

from django_descope import descope_client
from django_descope.conf import settings

logger = logging.getLogger(__name__)


class DescopeUser(auth.get_user_model()):  # type: ignore
    class Meta:
        proxy = True

    is_active = True
    """ User is always active since Descope will never issue a token for an inactive user. """

    def sync(self, session, refresh):
        self.session_token = session[SESSION_TOKEN_NAME]  # this should always exist
        self.refresh_token = refresh
        self.username = self._me.get("userId")
        self.user = self.username
        self.email = self._me.get("email")
        self.is_staff = descope_client.validate_roles(self.session_token, [settings.DESCOPE_IS_STAFF_ROLE])
        self.is_superuser = descope_client.validate_roles(self.session_token, [settings.DESCOPE_IS_SUPERUSER_ROLE])
        self.save()

    def __str__(self):
        return f"DescopeUser {self.username}"

    @property
    def _me(self):
        return cache.get_or_set(
            f"descope_me:{self.username}",  # noqa: E231
            lambda: descope_client.me(self.refresh_token),
        )

    def get_username(self):
        return self.username
