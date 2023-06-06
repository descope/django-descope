import logging

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View

logger = logging.getLogger(__name__)


class Logout(View):
    def get(self, request: HttpRequest):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class Index(View):
    def get(self, request: HttpRequest):
        logger.info("Index view called")
        return JsonResponse(
            {
                "user": request.user.username,
                "is_authenticated": request.user.is_authenticated,
                "is_staff": request.user.is_staff,
                "is_superuser": request.user.is_superuser,
                "email": request.user.email,
            }
        )
