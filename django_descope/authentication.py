import logging

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME, DescopeClient
from descope.exceptions import AuthException
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from .models import DescopeUser
from .settings import PROJECT_ID

logger = logging.getLogger(__name__)


class DescopeAuthentication(BaseBackend):
    _dclient = DescopeClient(PROJECT_ID)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request: HttpRequest):
        access_token = request.COOKIES.get(SESSION_COOKIE_NAME)
        refresh_token = request.COOKIES.get(REFRESH_SESSION_COOKIE_NAME)

        try:
            validated_token = self._dclient.validate_and_refresh_session(
                access_token, refresh_token
            )
        except AuthException:
            return None, None

        return self.get_user(request, validated_token, refresh_token), validated_token

    def get_user(self, request: HttpRequest, validated_token=None, refresh_token=None):
        if validated_token:
            user, created = DescopeUser.objects.get_or_create(
                username=validated_token.get("userId")
            )
            user.sync(validated_token, refresh_token)
            return user
        return None
