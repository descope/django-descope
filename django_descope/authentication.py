import logging

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME, DescopeClient
from descope.exceptions import AuthException
from django.contrib.auth import logout
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
        session = request.session.get(SESSION_COOKIE_NAME)
        refresh = request.session.get(REFRESH_SESSION_COOKIE_NAME)

        logger.debug("Validating (and refreshing) Descope session")
        logger.debug("session %s", session)
        logger.debug("refresh %s", refresh)
        try:
            validated_token = self._dclient.validate_and_refresh_session(
                session, refresh
            )
        except AuthException as e:
            """
            Ask forgiveness, not permission.
                - Grace Hopper

            This exception will be thrown on every unauthenticated request to
            ensure logging out an invalid user.
            """
            logger.debug(e)
            logout(request)
            return None

        logger.debug(validated_token)
        return self.get_user(request, validated_token, refresh)

    def get_user(self, request: HttpRequest, validated_token=None, refresh_token=None):
        if validated_token:
            username = validated_token.get("userId") or validated_token.get("sub")
            user, created = DescopeUser.objects.get_or_create(username=username)
            user.sync(validated_token, refresh_token)
            request.session[SESSION_COOKIE_NAME] = user.session
            return user
        return None
