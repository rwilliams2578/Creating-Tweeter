from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Simply adds a date of birth field.
    """

    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
