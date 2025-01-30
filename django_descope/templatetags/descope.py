import os

from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME
from django import template
from django.middleware.csrf import get_token as csrf_token
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from django_descope.conf import settings

register = template.Library()
CONTEXT_KEY = "descope_wc_included"


@register.simple_tag(takes_context=True)
def descope_flow(context, flow_id, success_redirect):
    script = ""
    if not context.get(CONTEXT_KEY):
        script += f'<script src="{settings.DESCOPE_WEB_COMPONENT_SRC}"></script>'
        context[CONTEXT_KEY] = True
    id = "descope-" + get_random_string(length=4)
    store_jwt_url = reverse("django_descope:store_jwt")
    flow = f"""
    <descope-wc id="{id}" project-id="{settings.DESCOPE_PROJECT_ID}"
     flow-id="{flow_id}" redirect-url="{context.request.build_absolute_uri()}"
        base-url="{os.environ.get('DESCOPE_BASE_URI', '')}"></descope-wc>
    <script>
        const descopeWcEle = document.getElementById('{id}');
        descopeWcEle.addEventListener('success', async (e) => {{
            const formData = new FormData();
            formData.append('{SESSION_COOKIE_NAME}', e.detail.sessionJwt);
            formData.append('{REFRESH_SESSION_COOKIE_NAME}',
                                e.detail.refreshJwt);
            formData.append('csrfmiddlewaretoken','{csrf_token(context.request)}')

            await fetch("{store_jwt_url}", {{
                method: "POST",
                body: formData,
            }})
            document.location.replace("{success_redirect}")
        }});
    </script>
    """  # noqa: E241, E222, E221, E702, E231, E202, E231, E272
    return mark_safe(script + flow)
