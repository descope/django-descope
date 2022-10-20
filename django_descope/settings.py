# flake8: noqa: E501
from inspect import getargs

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PROJECT_ID = getattr(settings, "DESCOPE_PROJECT_ID", None)
if not PROJECT_ID:
    raise ImproperlyConfigured('"DESCOPE_PROJECT_ID" is required!')

LOGIN_SENT_REDIRECT = getattr(
    settings, "DESCOPE_LOGIN_SENT_REDIRECT", "django_descope:login_sent"
)
LOGIN_TEMPLATE_NAME = getattr(
    settings, "DESCOPE_LOGIN_TEMPLATE_NAME", "django_descope/login.html"
)
LOGIN_SENT_TEMPLATE_NAME = getattr(
    settings, "DESCOPE_LOGIN_SENT_TEMPLATE_NAME", "django_descope/login_sent.html"
)
LOGIN_FAILED_TEMPLATE_NAME = getattr(
    settings, "DESCOPE_LOGIN_FAILED_TEMPLATE_NAME", "django_descope/login_failed.html"
)
SIGNUP_TEMPLATE_NAME = getattr(
    settings, "DESCOPE_SIGNUP_TEMPLATE_NAME", "django_descope/signup.html"
)
LOGIN_SUCCESS_REDIRECT = getattr(
    settings, "DESCOPE_LOGIN_SUCCESS_REDIRECT", "django_descope:show_tokens"
)

# If this setting is set to False a user account will be created the first time
# a user requests a login link.
REQUIRE_SIGNUP = getattr(settings, "DESCOPE_REQUIRE_SIGNUP", True)
if not isinstance(REQUIRE_SIGNUP, bool):
    raise ImproperlyConfigured('"DESCOPE_REQUIRE_SIGNUP" must be a boolean')

# Role names to create in Descope that will map to User attributes
IS_STAFF_ROLE = getattr(settings, "DESCOPE_IS_STAFF_ROLE", "is_staff")
IS_SUPERUSER_ROLE = getattr(settings, "DESCOPE_IS_SUPERUSER_ROLE", "is_superuser")
