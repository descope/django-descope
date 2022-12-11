from typing import Dict

from descope import (
    COOKIE_DATA_NAME,
    REFRESH_SESSION_COOKIE_NAME,
    REFRESH_SESSION_TOKEN_NAME,
    SESSION_COOKIE_NAME,
    SESSION_TOKEN_NAME,
)
from django.http import HttpResponse

from . import settings


def set_cookies(response: HttpResponse, jwt_response: Dict):
    access = jwt_response.get(SESSION_TOKEN_NAME)
    refresh = jwt_response.get(REFRESH_SESSION_TOKEN_NAME)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=access.get("jwt"),
        expires=jwt_response.get(COOKIE_DATA_NAME, {}).get("exp"),
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )

    if refresh:
        response.set_cookie(
            key=REFRESH_SESSION_COOKIE_NAME,
            value=refresh.get("jwt"),
            expires=jwt_response.get(COOKIE_DATA_NAME, {}).get("exp"),
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )


def delete_cookies(response: HttpResponse):
    response.delete_cookie(REFRESH_SESSION_COOKIE_NAME)
    response.delete_cookie(SESSION_COOKIE_NAME)
