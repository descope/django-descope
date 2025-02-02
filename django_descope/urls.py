from django.urls import path

from django_descope import views

app_name = "django_descope"

urlpatterns = [
    path("store_jwt", views.StoreJwt.as_view(), name="store_jwt"),
]
