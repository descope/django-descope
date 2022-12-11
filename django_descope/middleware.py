import logging

from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from .authentication import DescopeAuthentication
from .utils import delete_cookies, set_cookies

logger = logging.getLogger(__name__)


class DescopeMiddleware:
    _auth = DescopeAuthentication()

    def __init__(self, get_response: HttpResponse = None):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response: HttpResponse = self.get_response(request)

        if request.get_full_path() == reverse("admin:logout"):
            logout(request)
            delete_cookies(response)
            return response

        user, jwt = self._auth.authenticate(request=request)
        if user:
            login(request, user)
            response = self.get_response(request)
            set_cookies(response, jwt)

        return response
