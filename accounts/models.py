from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Customuser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
