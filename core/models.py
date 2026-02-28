from django.db import models
from django.contrib.auth.models import AbstractUser


# 👤 Custom User
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    preferred_language = models.CharField(max_length=20, default='en')


# 📝 Post (Text + Voice + Multilingual Ready)
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)
    voice_file = models.FileField(upload_to='voice_posts/', blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    original_language = models.CharField(max_length=20, default='en')
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.content and not self.voice_file:
            raise ValidationError("Post must contain text or voice.")

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"


# 👥 Follow System
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')