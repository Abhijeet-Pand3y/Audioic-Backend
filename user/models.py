from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#https://docs.djangoproject.com/en/4.1/topics/auth/customizing/
#Using custom user model
class User(AbstractUser):
    first_name = models.CharField(max_length = 100 )
    last_name = models.CharField(max_length= 100)
    #name will be taken as username
    uname = models.CharField(max_length = 50, unique = True)
    email = models.CharField(max_length = 200, unique = True)
    #default username to none because using email while logging in
    username = None
    # changing default login by username to email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # phone = models.CharField(max_length = 30, blank = True, null = True)
    user_photo = models.ImageField(upload_to= 'images/', blank= True, null= True)
    is_verified = models.BooleanField(default=False)   

    is_deleted = models.BooleanField(default=False)    
    #verification_code = models.CharField(default=0, max_length=6) 
    
    # expired for session token in case user closes the site before logging out
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserVerify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6,default='0')

    expired_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserToken(models.Model):
    token = models.CharField(max_length=36, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



