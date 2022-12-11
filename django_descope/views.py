import logging

from descope import (
    REFRESH_SESSION_COOKIE_NAME,
    SESSION_COOKIE_NAME,
    AuthException,
    DeliveryMethod,
    DescopeClient,
)
from django.conf import settings as django_settings
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, View
from django.views.generic.base import RedirectView

from . import settings, utils
from .forms import LoginForm, SignupForm

# User = get_user_model()
logger = logging.getLogger(__name__)

descope_client = DescopeClient(project_id=settings.PROJECT_ID)


@method_decorator(csrf_protect, name="dispatch")
class Login(TemplateView):
    template_name = settings.LOGIN_TEMPLATE_NAME

    def get(self, request: HttpRequest, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["require_signup"] = settings.REQUIRE_SIGNUP
        return self.render_to_response(context)

    def post(self, request: HttpRequest, *args, **kwargs):
        # logout(request)
        context = self.get_context_data(**kwargs)
        context["require_signup"] = settings.REQUIRE_SIGNUP
        form = LoginForm(request.POST)
        if not form.is_valid():
            context["login_form"] = form
            return self.render_to_response(context)

        email = form.cleaned_data.get("email")
        try:
            descope_client.magiclink.sign_in(
                DeliveryMethod.EMAIL,
                email,
                uri=request.build_absolute_uri(reverse("django_descope:login_verify")),
            )
            logger.info("Requested magiclink siginin for %s", email)
        except AuthException as e:
            form.add_error("email", str(e))
            context["login_form"] = form
            return self.render_to_response(context)

        return HttpResponseRedirect(reverse(settings.LOGIN_SENT_REDIRECT))


class LoginSent(TemplateView):
    template_name = settings.LOGIN_SENT_TEMPLATE_NAME


@method_decorator(never_cache, name="dispatch")
class LoginVerify(TemplateView):
    template_name = settings.LOGIN_FAILED_TEMPLATE_NAME

    def get(self, request: HttpRequest, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = request.GET.get("t")
        try:
            jwt_response = descope_client.magiclink.verify(token)
        except AuthException as e:
            context["login_error"] = e.error_message
            return self.render_to_response(context)

        logger.debug("Login successful, JWT: %s", jwt_response)

        response = HttpResponseRedirect(reverse(settings.LOGIN_SUCCESS_REDIRECT))

        utils.set_cookies(response, jwt_response)

        return response


@method_decorator(csrf_protect, name="dispatch")
class Signup(TemplateView):
    template_name = settings.SIGNUP_TEMPLATE_NAME

    def get(self, request: HttpRequest, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["signup_form"] = SignupForm()
        return self.render_to_response(context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = SignupForm(request.POST)
        if not form.is_valid():
            logger.warning("Signup form invalid")
            context["signup_form"] = form
            return self.render_to_response(context)

        email = form.cleaned_data.get("email")
        try:
            descope_client.magiclink.sign_up_or_in(
                DeliveryMethod.EMAIL,
                email,
                uri=request.build_absolute_uri(reverse("django_descope:login_verify")),
            )
            logger.info("Requested magiclink siginup for %s", email)
        except AuthException as e:
            form.add_error("email", str(e))
            context["login_form"] = form
            return self.render_to_response(context)

        return HttpResponseRedirect(reverse(settings.LOGIN_SENT_REDIRECT))


class Logout(RedirectView):
    def get(self, request: HttpRequest, *args, **kwargs):

        next_page = request.GET.get("next")
        if not next_page:
            next_page = reverse(django_settings.LOGOUT_REDIRECT_URL)

        response = HttpResponseRedirect(next_page)
        response.delete_cookie(REFRESH_SESSION_COOKIE_NAME)
        response.delete_cookie(SESSION_COOKIE_NAME)
        return response


class ShowTokens(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return JsonResponse(
            {
                "session": request.COOKIES.get(SESSION_COOKIE_NAME),
                "refresh": request.COOKIES.get(REFRESH_SESSION_COOKIE_NAME),
            }
        )
