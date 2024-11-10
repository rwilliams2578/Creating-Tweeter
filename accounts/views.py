from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class SignUpView(CreateView):
    """
    View for user registration.
    """

    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class UserProfileView(LoginRequiredMixin, UpdateView):
    """
    View for updating user profile information.
    Requires user to be logged in.
    """

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        """
        Returns the current user's profile.
        """
        return self.request.user


class CustomPasswordChangeView(PasswordChangeView):
    """
    View for changing password.
    """

    success_url = reverse_lazy("profile")
