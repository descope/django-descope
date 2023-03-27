import logging

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME, DescopeClient
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from . import settings

# User = get_user_model()
logger = logging.getLogger(__name__)

descope_client = DescopeClient(project_id=settings.PROJECT_ID)


@method_decorator([never_cache], name="dispatch")
class StoreJwt(View):
    def post(self, request: HttpRequest):
        session = request.POST.get(SESSION_COOKIE_NAME)
        refresh = request.COOKIES.get(REFRESH_SESSION_COOKIE_NAME)
        if not refresh:
            refresh = request.POST.get(REFRESH_SESSION_COOKIE_NAME)

        if session and refresh:
            request.session[SESSION_COOKIE_NAME] = session
            request.session[REFRESH_SESSION_COOKIE_NAME] = refresh
            return JsonResponse({"success": True})

        return HttpResponseBadRequest()
