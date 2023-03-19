import email
import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
import re
import random
from django.contrib.auth import get_user_model, login, logout
from .models import User, UserVerify, UserToken
from .serializers import UserSerializers
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
import uuid
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .authentication import CustomAuthentication
from rest_framework.authentication import BasicAuthentication
from .renderers import CustomRenderer
from django.utils import timezone

# Create your views here.

def generateSessionToken():
    
    rndstr = str(uuid.uuid4())

    return rndstr

@api_view(['GET',])
@authentication_classes([CustomAuthentication,])
@permission_classes([IsAuthenticated,])
@renderer_classes([CustomRenderer,])
def get_user_photo(request):
    
    try: 
        user = request.user
        image = user.user_photo
        return Response(image.file, content_type='image/png')

    except:
        return JsonResponse({"error":"User doesn't exist"})



@api_view(['POST',])
def signin(request):
    # if request.method != "POST":
    #     return JsonResponse({'error': 'Send POST request with valid parameters'})
    body = json.loads(request.body)

    username = body['email']
    password = body['password']

    #email validation 
    if not re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", username):
        return JsonResponse({'error': 'Enter Valid email.'})

   

    try:
        user = User.objects.filter(email=username).get()
    except:
        return JsonResponse({'error': 'Invalid Email'})
    try:
        if user.check_password(password):
            user_serializer = UserSerializers(user)
            user_dict = user_serializer.data
            # user_dict.pop('password')

            #checking if session token was reset during logging out to generate new session token
            date1 = timezone.now() + timezone.timedelta(weeks=2)
            token1 = generateSessionToken()
            token = UserToken.objects.create(user=user,token=token1,expired_at=date1)
            token.save()

            user_dict.update({"token":token1})

            #login(request, user)

            return JsonResponse({'user':user_dict})
        else:
            return JsonResponse({'error':'Invalid Password'})
    except:
        return JsonResponse({'error':'Unknown error occured please try again'})


@api_view(['GET',])
def signout(request):
    #logout(request)

    token = request.GET.get('token', '0')
    if token == '0':
        return JsonResponse({"error":"invalid token"})

    try:
        token = UserToken.objects.filter(token=token).get()
        token.delete()
    except:
        return JsonResponse({'error': 'token not found'})

    return JsonResponse({'success': 'Logout Success'})

@api_view(['POST',])
@csrf_exempt
def signup(request):
    # username = request.POST.get("email", "onasde@gmail.com")
    # password = request.POST.get("password","None@123")
    # first_name= request.POST.get("first_name","None")
    # last_name= request.POST.get("last_name","None")
    # uname= request.POST.get("uname","None")   
    #body = json.loads(request.body)
    #username = body["email"]
    # password = body["password"]
    # first_name= body["first_name"]
    # last_name= body["last_name"]
    # uname= body["uname"]
    username = request.POST["email"]
    password = request.POST["password"]
    first_name= request.POST["first_name"]
    last_name= request.POST["last_name"]
    uname= request.POST["uname"]

    # #user_photo may be in complete TODO 
    user_photo = request.FILES.get("image_field",None)

    #email validation
    email_regex = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"   
    if not re.fullmatch(email_regex, username):
        return JsonResponse({'error': 'Enter Valid email.'})

    #password validation 
    # - at least 8 characters
    # - must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number
    # - Can contain special characters
    password_regrex = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
    if not re.fullmatch(password_regrex, password):
         return JsonResponse({'error': 'Password must be at least 8 characters, must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number'})
    
    if len(uname)<=3:
        return JsonResponse({'error':'Username must be more than 3 characters.'})
    
    #Checking if email already exixts
    try:
        UserModel = User.objects.get(email=username)
        return JsonResponse({'error':'Email already exists'})
    except:
        pass
    
    #Checking if username is unique
    try:
        UserModel = User.objects.get(uname=uname)
        return JsonResponse({'error':'Username already exists'})
    except:
        pass
    
    instance = User(uname = uname, email = username, first_name = first_name, last_name = last_name, user_photo = user_photo)
    instance.set_password(password)
    instance.save()

    
    verify_user = UserVerify(user_id = instance.id , verification_code = "0")
    verify_user.save()

    return JsonResponse({'success':'Signup Success'})


@api_view(["GET",])
@authentication_classes([CustomAuthentication,])
@permission_classes([IsAuthenticated])
def send_verification_code(request):
    
    
    email_address = request.GET['email']
    token1 = request.GET['token']
    try:
        user = User.objects.get(email = email_address)
        token = UserToken.objects.get(token = token1)
    except:
        return JsonResponse({'error':'email not registered.'})

    if token.token == '0':
        return JsonResponse({'error':'User not logged in. Try logging in first'})

    if user.is_verified is not False:
        return JsonResponse({'error':'User already verified'})
    
    else:
        userid = user.id

        try:
            verify_user = UserVerify.objects.get(user_id = userid)
        except:
            return JsonResponse({"error":"user not found"})

        vcode = generateVerificationCode()
        verify_user.verification_code = vcode
        verify_user.save()
    
    try:
        send_mail(
            subject="Verification Code From Audioic",
            message=vcode,
            from_email='audioic69@outlook.com',
            recipient_list=[email_address,],
        ) 
        return JsonResponse({'success':'verification code sent'})
    except:
        return JsonResponse({'error':'email not sent'})

@api_view(['GET',])
def receive_verification_code(request):
    token1 = request.GET['token']
    vcode = request.GET['vcode']
    
    if token1 == '0':
        return JsonResponse({'error':'User session expired. Try to relogin'})
    try:
        token = UserToken.objects.get(token = token1)
        user = User.objects.get(id = token.user_id)
    except:
        return JsonResponse({'error':'User session expired. Try to relogin'})
    
    try:
        verify_user = UserVerify.objects.get(user_id = user.id)
    except:
        return JsonResponse({"error":"user not found"})

    if verify_user.verification_code == vcode:
        user.is_verified = True
        verify_user.delete()
        user.save()
        return JsonResponse({'success':'User Verified'})
    else:
        return JsonResponse({'invalid_code':'Your code does not match'})
    
    

    
def generateVerificationCode():
    rndlist = ['0','1','2','3','4','5','6','7','8','9']

    rnd = ''

    for _ in range(6):
        rnd = rnd + random.SystemRandom().choice(rndlist)
    
    return rnd

@api_view(["GET",])
@authentication_classes([CustomAuthentication,])
@permission_classes([IsAuthenticated,])
def testFunction(request):
    
    user = request.user
    token = request.GET["token"]

    return JsonResponse({"h":token, "user":user})

@api_view(["POST"])
@authentication_classes([CustomAuthentication,])
@permission_classes([IsAuthenticated,])
def changePassword(request):

    user = request.user
    current_password = request.POST["current_password"]
    new_password = request.POST["new_password"]

    if user.check_password(current_password):
        user.set_password(new_password)
        user.save()
        return JsonResponse({"success":"Password Updated"})
    else:
        return JsonResponse({"error":"Password didnt match"})

