from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import json
from .models import User, UserToken
from django.utils import timezone

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):

        # body = json.loads(request.body)

        if request.method == "GET":
            token1 = request.GET["token"]
        if request.method == "POST":
            token1 = request.POST["token"]
        
        
        if token1 == "0":
            raise AuthenticationFailed("Authentication credentials do not match.")

        try:
            token = UserToken.objects.filter(token=token1).get()

        except:
            raise AuthenticationFailed("Invalid token")
        
        if token.expired_at < timezone.now():
                raise AuthenticationFailed("Login session has expired.")
                
        user = User.objects.filter(id=token.user_id).get()
        return (user, None)
        
        
            
    