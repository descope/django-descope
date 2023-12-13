import logging
from typing import Any, Union

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME, SESSION_TOKEN_NAME
from descope.exceptions import AuthException
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from . import descope_client
from .models import DescopeUser

logger = logging.getLogger(__name__)


def add_tokens_to_request(session: Any, session_token: str, refresh_token: str):
    session[SESSION_COOKIE_NAME] = session_token
    session[REFRESH_SESSION_COOKIE_NAME] = refresh_token
    session.save()


class DescopeAuthentication(BaseBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request: Union[HttpRequest, None], **kwargs):
        if request is None:
            return None
        session_token = request.session.get(SESSION_COOKIE_NAME, "")
        refresh_token = request.session.get(REFRESH_SESSION_COOKIE_NAME, "")

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
        if validated_session:
            username = validated_session[SESSION_TOKEN_NAME]["sub"]
            user, _ = DescopeUser.objects.get_or_create(username=username)
            user.sync(validated_session, refresh_token)
            request.session[SESSION_COOKIE_NAME] = user.session_token["jwt"]
            return user
        else:
            return None
