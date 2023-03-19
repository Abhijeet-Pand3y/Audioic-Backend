from django.db import models

# Create your models here.


class AudioBooks(models.Model):
    audioBook = models.CharField(max_length=50, null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)