"""
Name: Revelle Williams
Class: CIS 218
Date: November 28, 2024
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Simply adds a date of birth field.
    """

    date_of_birth = models.DateField(null=True, blank=True)
