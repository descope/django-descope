import logging

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse

from descope import (
    SESSION_TOKEN_NAME,
    AuthException,
    DescopeClient,
)


from . import settings

logger = logging.getLevelName(__name__)


def DescopeMiddleware(get_response):
    descope_client = DescopeClient(project_id=settings.PROJECT_ID)

    def middleware(request: HttpRequest) -> HttpResponse:
        """Descope request middleware

        This middlware inspects the session for an existing session and refresh token.

        On every request the session token is validated to ensure the JWT hasn't expired,
        in case it is expired, the validate call uses the refresh token to aquire a new session JWT
        and stores it in the user session.

        In any case where the session invalidates and cannot be renewed, the user is logged out.

        Args:
            request (HttpRequest): Django HTTP Request

        Returns:
            HttpResponse: Django HTTP Response
        """
        refresh_token: dict = request.session.get("descopeRefresh")
        session_token: dict = request.session.get("descopeSession")

        if not (refresh_token and session_token):
            logout(request)
            return get_response(request)
        try:
            jwt_response: dict = descope_client.validate_session_request(
                session_token.get("jwt"), refresh_token.get("jwt")
            )
            request.session["descopeSession"] = jwt_response[SESSION_TOKEN_NAME]
        except AuthException as e:
            logger.error(e)
            logout(request)

        return get_response(request)

    return middleware
