from django.urls import path
from django.views.generic import TemplateView

from .views import Debug

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="descope_login.html"),
        name="index",
    ),
    path("debug", Debug.as_view(), name="debug"),
]
