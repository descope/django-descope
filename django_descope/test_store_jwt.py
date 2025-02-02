import json
import logging
import random
import string

import django
from descope import (
    REFRESH_SESSION_COOKIE_NAME,
    REFRESH_SESSION_TOKEN_NAME,
    SESSION_COOKIE_NAME,
    SESSION_TOKEN_NAME,
    DeliveryMethod,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.test import TestCase, override_settings
from django.urls import path, reverse
from django.views import View

from django_descope import conf, descope_client, urls

logger = logging.getLogger(__name__)


def random_string(N: int) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=N))


class TestProtectedView(LoginRequiredMixin, View):
    def get(self, request):
        return JsonResponse({"success": True})


urls.urlpatterns = urls.urlpatterns + [
    path("test", TestProtectedView.as_view(), name="test_protected_view"),
]


@override_settings(ROOT_URLCONF=urls)
class StoreJwtTestCase(TestCase):
    delivery_method = DeliveryMethod.EMAIL
    login_id = f"test+{random_string(8)}@test.internal"
    token: dict

    def setUp(self) -> None:
        descope_client.mgmt.user.create_test_user(
            self.login_id,
            role_names=["is_staff", "is_superuser"],
            verified_email=True,
        )
        resp = descope_client.mgmt.user.generate_otp_for_test_user(
            self.delivery_method,
            self.login_id,
        )
        self.token = descope_client.otp.verify_code(self.delivery_method, self.login_id, resp.get("code"))

    @override_settings(DESCOPE_PROJECT_ID="")
    def test_no_project_id(self):
        """Test that the store_jwt view fails without a project_id"""
        with self.assertRaises(django.core.exceptions.ImproperlyConfigured):
            conf.settings.validate()

    def test_store_jwt(self):
        """Test the store_jwt view"""

        # should fail without a session
        res = self.client.get(reverse("test_protected_view"))
        self.assertNotEqual(res.status_code, 200)

        # lets store the jwt
        res = self.client.post(
            reverse("store_jwt"),
            {
                SESSION_COOKIE_NAME: self.token[SESSION_TOKEN_NAME]["jwt"],
                REFRESH_SESSION_COOKIE_NAME: self.token[REFRESH_SESSION_TOKEN_NAME]["jwt"],
            },
        )
        self.assertEqual(res.status_code, 200)

        debug = json.loads(res.content)
        self.assertEqual(debug["success"], True)
        session = self.client.session
        self.assertEqual(  # ensure the session was updated
            session[SESSION_COOKIE_NAME], self.token[SESSION_TOKEN_NAME]["jwt"]
        )
        self.assertEqual(  # ensure the session was updated
            session[REFRESH_SESSION_COOKIE_NAME],
            self.token[REFRESH_SESSION_TOKEN_NAME]["jwt"],
        )

        # should succeed with a session
        res = self.client.get(reverse("test_protected_view"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(debug["success"], True)

    def tearDown(self) -> None:
        descope_client.mgmt.user.delete(self.login_id)
