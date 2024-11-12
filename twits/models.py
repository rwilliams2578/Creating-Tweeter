from django.db import models
from django.conf import settings


class Twit(models.Model):
    """
    Model representing a Twit post.
    Each Twit has an author, body text, optional image URL, and timestamps.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_twits", blank=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_liked_by(self):
        """
        Returns whether the current user has liked this twit.
        """
        user = self.request.user if hasattr(self, "request") else None
        if user and user.is_authenticated:
            return self.likes.filter(id=user.id).exists()
        return False

    def __str__(self):
        """
        Returns a string representation of the Twit.
        """
        return f"{self.author.username}: {self.body[:50]}..."


class Comment(models.Model):
    """
    Model representing a comment on a Twit.
    """

    twit = models.ForeignKey("Twit", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username}: {self.body[:50]}"
