from django.urls import path
from django.views.generic import TemplateView

from .admin import descope_admin_site
from .views import Debug

urlpatterns = [
    path("", TemplateView.as_view(template_name="descope_login.html"), name="index"),
    path("admin/", descope_admin_site.urls, name="admin"),
    path("debug", Debug.as_view(), name="debug"),
]
