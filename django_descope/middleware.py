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
        refresh_token: dict = request.session.get('descopeRefresh')
        session_token: dict = request.session.get('descopeSession')
        
        if not (refresh_token and session_token):
            logout(request)
            return get_response(request)
        try:
            jwt_response: dict = descope_client.validate_session_request(session_token.get('jwt'), refresh_token.get('jwt'))
            request.session['descopeSession'] = jwt_response[SESSION_TOKEN_NAME]
        except AuthException as e:
            logger.error(e)
            raise e
        
        return get_response(request)

    return middleware