import logging

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME
from descope.exceptions import AuthException
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from django_descope import descope_client

from .models import DescopeUser

logger = logging.getLogger(__name__)


class DescopeAuthentication(BaseBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request: HttpRequest):
        session_token = request.session.get(SESSION_COOKIE_NAME)
        refresh_token = request.session.get(REFRESH_SESSION_COOKIE_NAME)

        logger.debug("Validating (and refreshing) Descope session")
        try:
            validated_session = descope_client.validate_and_refresh_session(
                session_token, refresh_token
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

        if settings.DEBUG:
            # Contains sensitive information, so only log in DEBUG mode
            logger.debug(validated_session)
        return self.get_user(request, validated_session, refresh_token)

    def get_user(self, request: HttpRequest, validated_session, refresh_token):
        if validated_session:
            username = validated_session.get("userId") or validated_session.get("sub")
            user, created = DescopeUser.objects.get_or_create(username=username)
            user.sync(validated_session, refresh_token)
            request.session[SESSION_COOKIE_NAME] = user.session_token["jwt"]
            return user
        return None
