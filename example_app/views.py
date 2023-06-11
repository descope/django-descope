import logging

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View

from django_descope.models import DescopeUser

logger = logging.getLogger(__name__)


class Logout(View):
    def get(self, request: HttpRequest):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class Debug(View):
    def get(self, request: HttpRequest):
        logger.info("Debug view called")
        return JsonResponse(
            {
                "user": request.user.username,
                "is_authenticated": request.user.is_authenticated,
                "is_staff": request.user.is_staff,
                "is_superuser": request.user.is_superuser,
                "email": request.user.email,
                "session": request.user.session,
            }
            if isinstance(request.user, DescopeUser)
            else {
                "is_authenticated": request.user.is_authenticated,
                "is_anonymous": request.user.is_anonymous,
                "is_active": request.user.is_active,
            }
        )
