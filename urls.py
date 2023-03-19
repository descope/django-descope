from django.urls import include, path
from django.views.generic import TemplateView

import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="descope_login.html"), name="index"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("django_descope.urls")),  # <-- Add the Descope URLs
]
