import json
import logging
import random
import string

import descope
from descope import REFRESH_SESSION_TOKEN_NAME, SESSION_TOKEN_NAME
from django.test import TestCase

from django_descope import descope_client
from django_descope.authentication import add_tokens_to_request

logger = logging.getLogger(__name__)


def random_string(N: int) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=N))


class AdminLoginTestCase(TestCase):
    delivery_method = descope.DeliveryMethod.EMAIL
    login_id = f"test+{random_string(8)}@test.internal"
    token: dict

    def setUp(self) -> None:
        descope_client.mgmt.user.create_test_user(
            self.login_id, role_names=["is_staff", "is_superuser"], verified_email=True
        )
        resp = descope_client.mgmt.user.generate_otp_for_test_user(
            self.delivery_method,
            self.login_id,
        )
        self.token = descope_client.otp.verify_code(
            self.delivery_method, self.login_id, resp.get("code")
        )

        session = self.client.session
        add_tokens_to_request(
            session,
            self.token[SESSION_TOKEN_NAME]["jwt"],
            self.token[REFRESH_SESSION_TOKEN_NAME]["jwt"],
        )

    def test_test_user_can_login_to_admin(self):
        """Test that if user has the right roles they can login to admin"""

        res = self.client.get("/debug")
        self.assertEqual(res.status_code, 200)

        debug = json.loads(res.content)
        self.assertEqual(debug["user"], self.token["userId"])
        self.assertEqual(debug["email"], self.login_id)
        self.assertTrue(debug["is_authenticated"])
        self.assertTrue(debug["is_staff"])
        self.assertTrue(debug["is_superuser"])

        res = self.client.get("/admin/")
        self.assertEqual(res.status_code, 200, res.headers)

    def tearDown(self) -> None:
        descope_client.mgmt.user.delete(self.login_id)
