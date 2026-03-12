from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username