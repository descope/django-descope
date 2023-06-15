import logging

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View

from django_descope import descope_client
from django_descope.models import DescopeUser
from django.shortcuts import render

from django.urls import path


logger = logging.getLogger(__name__)


class Logout(View):
    def get(self, request: HttpRequest):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class Debug(View):
    def get(self, request: HttpRequest):
        logger.info("Debug view called")
        mgmt = False
        try:
            descope_client.mgmt
            mgmt = True
        except Exception:
            pass

        return JsonResponse(
            {
                "user": request.user.username,
                "is_authenticated": request.user.is_authenticated,
                "is_staff": request.user.is_staff,
                "is_superuser": request.user.is_superuser,
                "email": request.user.email,
                "session": request.user.session_token,
                "is_mgmt_available": mgmt,
            }
            if isinstance(request.user, DescopeUser)
            else {
                "is_authenticated": request.user.is_authenticated,
                "is_anonymous": request.user.is_anonymous,
                "is_active": request.user.is_active,
            }
        )
