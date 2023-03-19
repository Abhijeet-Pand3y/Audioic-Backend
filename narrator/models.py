from django.db import models
from audiobooks.models import AudioBooks

# Create your models here.

class Narrator(models.Model):
    first_name = models.CharField(max_length=100, default = "Not Set")
    last_name = models.CharField(max_length=100, default = "Not Set")
    middle_name = models.CharField(max_length=100, default = "Not Set",null=True,blank=True)
    description = models.CharField(max_length = 2000, null=True, blank = True)
    facebook_id = models.CharField(max_length = 150, default="Not Set")
    instagram_id = models.CharField(max_length = 150, default="Not Set")
    twitter_id = models.CharField(max_length = 150, default="Not Set")
    photo = models.ImageField(upload_to='images/narrator', blank = True, null = True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class NarratedBooks(models.Model):
    narrator = models.ForeignKey(Narrator, on_delete=models.SET_NULL, blank= True, null=True)
    booksNarated = models.ForeignKey(AudioBooks, on_delete=models.CASCADE, null= True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)