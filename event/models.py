from django.db import models


# Create your models here.
class Events(models.Model):
    name = models.CharField(max_length=50)
    detail = models.CharField(max_length=500)
    organizer = models.CharField(max_length=50)
    date = models.DateTimeField()
    location = models.CharField(max_length=50)

    is_completed = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)