from django import forms
from django.contrib.auth import get_user_model

from . import settings

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"autofocus": "autofocus", "placeholder": "Enter your email"}
        )
    )

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if settings.REQUIRE_SIGNUP:
                error = "We could not find a user with that email address"
                raise forms.ValidationError(error)
        else:
            is_active = getattr(user, "is_active", True)
            if not is_active:
                raise forms.ValidationError("This user has been deactivated")

        return email


class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            error = "Email address is already linked to an account"
            is_active = getattr(user, "is_active", True)
            if not is_active:
                error = "This user has been deactivated"
            raise forms.ValidationError(error)
