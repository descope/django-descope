from descope import REFRESH_SESSION_COOKIE_NAME, SESSION_COOKIE_NAME
from django import template
from django.middleware.csrf import get_token as csrf_token
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from ..settings import PROJECT_ID, WEB_COMPONENT_SRC

register = template.Library()
CONTEXT_KEY = "descope_wc_included"


@register.simple_tag(takes_context=True)
def descope_flow(context, flow_id):
    script = ""
    if not context.get(CONTEXT_KEY):
        script += f'<script src="{WEB_COMPONENT_SRC}"></script>'
        context[CONTEXT_KEY] = True
    id = "descope-" + get_random_string(length=4)
    store_jwt_url = reverse("django_descope:store_jwt")
    flow = f"""
    <descope-wc id="{id}" project-id="{PROJECT_ID}" flow-id="{flow_id}"></descope-wc>
    <script>
        const descopeWcEle = document.getElementById('{id}');
        descopeWcEle.addEventListener('success', (e) => {{
            console.dir(e.detail);
            const formData = new FormData();
            formData.append('{SESSION_COOKIE_NAME}', e.detail.sessionJwt);
            formData.append('{REFRESH_SESSION_COOKIE_NAME}', e.detail.refreshJwt);
            formData.append('csrfmiddlewaretoken','{csrf_token(context.request)}')

            fetch("{store_jwt_url}", {{
                method: "POST",
                body: formData,
            }})
        }});
    </script>
    """
    return mark_safe(script + flow)
