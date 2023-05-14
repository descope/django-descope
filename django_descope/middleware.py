import logging

from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse

from .authentication import DescopeAuthentication

logger = logging.getLogger(__name__)


class DescopeMiddleware:
    _auth = DescopeAuthentication()

    def __init__(self, get_response: HttpResponse = None):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        user = self._auth.authenticate(request)
        if user:
            login(request, user)
        return self.get_response(request)
