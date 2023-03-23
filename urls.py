from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="descope_login.html")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("django_descope.urls")),  # <-- Add the Descope URLs
]
