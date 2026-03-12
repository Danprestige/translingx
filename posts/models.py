from django.db import models
from django.conf import settings


class Post(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    text = models.TextField(blank=True)

    voice = models.FileField(
        upload_to="voice_posts/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user}"