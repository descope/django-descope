import logging

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from django_descope.authentication import add_tokens_to_request

logger = logging.getLogger(__name__)


@method_decorator([never_cache], name="dispatch")
class StoreJwt(View):
    def post(self, request: HttpRequest):
        session = request.POST.get(SESSION_COOKIE_NAME)
        refresh = request.COOKIES.get(REFRESH_SESSION_COOKIE_NAME)
        if not refresh:
            refresh = request.POST.get(REFRESH_SESSION_COOKIE_NAME)

        if session and refresh:
            add_tokens_to_request(request.session, session, refresh)
            return JsonResponse({"success": True})

        return HttpResponseBadRequest()
