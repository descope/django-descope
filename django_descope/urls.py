from django.urls import path

from . import views

app_name = "django_descope"

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("login/sent/", views.LoginSent.as_view(), name="login_sent"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("login/verify/", views.LoginVerify.as_view(), name="login_verify"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("tokens/", views.ShowTokens.as_view(), name="show_tokens"),
]
