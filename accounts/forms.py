from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user with date of birth field.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")  # Removed first_name and last_name
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user profile information.
    """

    password = None  # Remove password field from the form

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
        )  # Keep all fields for profile editing
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom password reset form with styled fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control"})
