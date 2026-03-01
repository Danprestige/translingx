from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    preferred_language = models.CharField(max_length=5, default='en')  # e.g., 'en', 'fr', 'es'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='post_audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"