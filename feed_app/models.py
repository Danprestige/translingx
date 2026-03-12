from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"