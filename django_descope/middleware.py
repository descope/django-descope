import logging

from django.contrib.auth import login
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from django_descope.authentication import DescopeAuthentication

logger = logging.getLogger(__name__)


class DescopeMiddleware(MiddlewareMixin):
    _auth = DescopeAuthentication()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        user = self._auth.authenticate(request)
        if user:
            login(request, user)
        return self.get_response(request) if self.get_response else None
