from django.urls import include, path

import example_app.views as views

urlpatterns = [
    path("", include("example_app.urls")),
    path("logout", views.Logout.as_view(), name="logout"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("django_descope.urls")),  # <-- Add the Descope URLs
]
