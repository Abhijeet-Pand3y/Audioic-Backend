from django.db import models
from api.audiobooks.models import AudioBooks


class Author(models.Model):
    name = models.CharField(max_length=100, default="Not Set")
    description = models.CharField(max_length = 2000, null=True, blank = True)
    facebook_id = models.CharField(max_length = 150, default="Not Set")
    instagram_id = models.CharField(max_length = 150, default="Not Set")
    twitter_id = models.CharField(max_length = 150, default="Not Set")
    photo = models.ImageField(upload_to='images/', blank = True, null = True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AuthoredBooks(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank= True, null=True)
    books_authored = models.ForeignKey(AudioBooks, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

