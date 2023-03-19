from django.urls import path

from . import views

app_name = "django_descope"

urlpatterns = [
    path("store_jwt", views.StoreJwt.as_view(), name="store_jwt"),
]
