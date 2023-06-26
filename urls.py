from django.contrib import admin
from django.urls import include, path

import example_app.views as views

# (optional) override the login template with descope flow
descope_admin_site = admin.site
descope_admin_site.login_template = "admin/descope_login.html"

urlpatterns = [
    path("", include("example_app.urls")),
    path("logout", views.Logout.as_view(), name="logout"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("django_descope.urls")),  # <-- Add the Descope URLs
    # (optional) override django admin login
    path("admin/", descope_admin_site.urls),
]
