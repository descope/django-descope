from django.urls import path
from django.views.generic import TemplateView

from .views import Index

urlpatterns = [
    path("", TemplateView.as_view(template_name="descope_login.html"), name="index"),
    path("test", Index.as_view(), name="test"),
]
