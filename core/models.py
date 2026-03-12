# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )


class Post(models.Model):
    title = models.CharField(max_length=255, default="Untitled Post")
    content = models.TextField(default="")
    author = models.ForeignKey("core.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title