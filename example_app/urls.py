from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
from .views import Debug
from .admin import descope_admin_site
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", TemplateView.as_view(template_name="descope_login.html"), name="index"),
    path('admin/', descope_admin_site.urls, name="admin"),
    path("debug", Debug.as_view(), name="debug"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
