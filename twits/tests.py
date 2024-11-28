"""
Name: Revelle Williams
Class: CIS 218
Date: November 28, 2024
"""

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from .models import Twit, Comment


class TweeterTests(TestCase):
    """
    Tests for Tweeter functionality including authentication,
    twits, comments, and likes.
    """

    def test_twit_creation(self):
        """Test creating a new twit"""
        # Create a user
        user = CustomUser.objects.create_user(username="testuser", password="testPass@123")

        # Log in
        self.client.login(username="testuser", password="testPass@123")

        # Create a twit
        twit_data = {"body": "Test twit content", "image_url": "https://example.com/image.jpg"}
        response = self.client.post(reverse("twit_create"), twit_data)

        # Check twit was created
        self.assertEqual(Twit.objects.count(), 1)
        twit = Twit.objects.first()
        self.assertEqual(twit.body, "Test twit content")
        self.assertEqual(twit.author, user)

    def test_twit_editing(self):
        """Test editing a twit"""
        # Create user and twit
        user = CustomUser.objects.create_user(username="testuser", password="testPass@123")
        twit = Twit.objects.create(author=user, body="Original content")

        # Log in
        self.client.login(username="testuser", password="testPass@123")

        # Edit twit
        edit_data = {"body": "Updated content"}
        response = self.client.post(reverse("twit_update", kwargs={"pk": twit.pk}), edit_data)

        # Verify twit was updated
        twit.refresh_from_db()
        self.assertEqual(twit.body, "Updated content")

    def test_comment_creation(self):
        """Test adding a comment to a twit"""
        # Create user and twit
        user = CustomUser.objects.create_user(username="testuser", password="testPass@123")
        twit = Twit.objects.create(author=user, body="Test twit")

        # Log in
        self.client.login(username="testuser", password="testPass@123")

        # Add comment
        comment_data = {"body": "Test comment"}
        response = self.client.post(reverse("comment_new", kwargs={"pk": twit.pk}), comment_data)

        # Verify comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "Test comment")
        self.assertEqual(comment.twit, twit)
        self.assertEqual(comment.author, user)

    def test_like_functionality(self):
        """Test liking and unliking twits"""
        # Create users and twit
        user1 = CustomUser.objects.create_user(username="user1", password="testPass@123")
        user2 = CustomUser.objects.create_user(username="user2", password="testPass@123")
        twit = Twit.objects.create(author=user1, body="Test twit")

        # Test like as user2
        self.client.login(username="user2", password="testPass@123")
        response = self.client.post(reverse("like_twit", kwargs={"pk": twit.pk}))
        self.assertEqual(twit.likes.count(), 1)

        # Test unlike
        response = self.client.post(reverse("like_twit", kwargs={"pk": twit.pk}))
        self.assertEqual(twit.likes.count(), 0)

    def test_twit_delete(self):
        """Test deleting a twit"""
        # Create user and twit
        user = CustomUser.objects.create_user(username="testuser", password="testPass@123")
        twit = Twit.objects.create(author=user, body="Test twit")

        # Log in and delete twit
        self.client.login(username="testuser", password="testPass@123")
        response = self.client.post(reverse("twit_delete", kwargs={"pk": twit.pk}))

        # Verify twit was deleted
        self.assertEqual(Twit.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test that users can't edit/delete others' twits"""
        # Create two users and a twit
        user1 = CustomUser.objects.create_user(username="user1", password="testPass@123")
        user2 = CustomUser.objects.create_user(username="user2", password="testPass@123")
        twit = Twit.objects.create(author=user1, body="Test twit")

        # Try to edit as user2
        self.client.login(username="user2", password="testPass@123")
        edit_response = self.client.post(reverse("twit_update", kwargs={"pk": twit.pk}), {"body": "Hacked content"})
        delete_response = self.client.post(reverse("twit_delete", kwargs={"pk": twit.pk}))

        # Verify access was denied
        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        twit.refresh_from_db()
        self.assertEqual(twit.body, "Test twit")  # Content unchanged
