import logging

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME, DescopeClient
from descope.exceptions import AuthException
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from .models import DescopeUser
from .settings import PROJECT_ID

logger = logging.getLogger(__name__)


class DescopeAuthentication(BaseBackend):
    descope = DescopeClient(project_id=PROJECT_ID)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request: HttpRequest):
        session = request.session.get(SESSION_COOKIE_NAME)
        refresh = request.session.get(REFRESH_SESSION_COOKIE_NAME)

        logger.debug("Validating (and refreshing) Descope session")
        try:
            validated_session = self.descope.validate_and_refresh_session(
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

        if settings.DEBUG:
            # Contains sensitive information, so only log in DEBUG mode
            logger.debug(validated_session)
        return self.get_user(request, validated_session, refresh)

    def get_user(self, request: HttpRequest, session=None, refresh=None):
        if session:
            username = session.get("userId") or session.get("sub")
            user, created = DescopeUser.objects.get_or_create(username=username)
            user.sync(session, refresh)
            request.session[SESSION_COOKIE_NAME] = user.token
            return user
        return None
