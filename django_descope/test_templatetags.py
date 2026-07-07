import logging

from django.template import Context
from django.test import RequestFactory, TestCase, override_settings
from django.utils.safestring import SafeString

from django_descope.templatetags.descope import CONTEXT_KEY, descope_flow

logger = logging.getLogger(__name__)

TEST_PROJECT_ID = "P2TestProjectId0000000000000000"


@override_settings(ROOT_URLCONF="urls", DESCOPE_PROJECT_ID=TEST_PROJECT_ID)
class DescopeFlowTagTestCase(TestCase):
    """Offline tests for the ``descope_flow`` template tag.

    These exercise Django template, CSRF, URL reversing and safestring APIs
    without any network calls to Descope, so they run under every supported
    Django version (including Django 6.0).
    """

    def _context(self):
        context = Context({})
        # ``descope_flow`` takes_context and reads ``context.request``.
        context.request = RequestFactory().get("/")
        return context

    def test_returns_marked_safe_html(self):
        """The tag output must be marked safe so it is not auto-escaped."""
        html = descope_flow(self._context(), "sign-up-or-in", "/")
        self.assertIsInstance(html, SafeString)

    def test_renders_web_component_and_flow(self):
        """The rendered markup includes the web component and the flow config."""
        html = descope_flow(self._context(), "sign-up-or-in", "/")

        # Web component script is included on first render.
        self.assertIn("@descope/web-component@", html)
        # The flow element is rendered with the configured project and flow id.
        self.assertIn("<descope-wc", html)
        self.assertIn(f'project-id="{TEST_PROJECT_ID}"', html)
        self.assertIn('flow-id="sign-up-or-in"', html)
        # The success handler posts back to the namespaced store_jwt URL.
        self.assertIn("/auth/store_jwt", html)

    def test_web_component_included_only_once_per_context(self):
        """Reusing the same context must not inject the script tag twice."""
        context = self._context()

        first = descope_flow(context, "sign-up-or-in", "/")
        self.assertIn("@descope/web-component@", first)
        self.assertTrue(context.get(CONTEXT_KEY))

        second = descope_flow(context, "another-flow", "/")
        # Script tag is only emitted on the first render for a given context.
        self.assertNotIn("<script src=", second)
        # ...but the flow element is still rendered.
        self.assertIn('flow-id="another-flow"', second)
