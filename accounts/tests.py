"""
Name: Revelle Williams
Class: CIS 218
Date: November 28, 2024
"""

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from .models import Twit, Comment


class AccountTests(TestCase):
    """
    Tests for Tweeter functionality including authentication,
    twits, comments, and likes.
    """

    def test_signup(self):
        """Test user registration"""
        # Create new user data
        user_data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password1": "testPass@123",
            "password2": "testPass@123",
            "date_of_birth": "2000-01-01",
        }

        # Test signup
        response = self.client.post(reverse("signup"), user_data)
        # Should redirect after success
        self.assertEqual(response.status_code, 302)

        # Verify user was created
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())

    def test_login_required(self):
        """Test that protected pages require login"""
        # Try to access protected pages
        dashboard_response = self.client.get(reverse("dashboard"))
        profile_response = self.client.get(reverse("profile"))

        # Should redirect to login
        self.assertEqual(dashboard_response.status_code, 302)
        self.assertEqual(profile_response.status_code, 302)

    def test_public_profile(self):
        """Test viewing a user's public profile"""
        # Create user and twits
        user = CustomUser.objects.create_user(username="testuser", password="testPass@123")
        Twit.objects.create(author=user, body="First twit")
        Twit.objects.create(author=user, body="Second twit")

        # View profile
        response = self.client.get(reverse("public_profile", kwargs={"pk": user.pk}))

        # Verify response and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["twits"]), 2)
