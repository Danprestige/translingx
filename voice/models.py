from django.db import models
from streams.models import Post


class VoiceProcessing(models.Model):

    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE
    )

    transcript = models.TextField(blank=True)

    translated_text = models.TextField(blank=True)

    processed = models.BooleanField(default=False)