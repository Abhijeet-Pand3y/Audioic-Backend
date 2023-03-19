# from lib2to3.pgen2 import token
# from django.test import TestCase

# # def hell(new,old):
# #     print("this is "+ new +" and this is old " + old)

# # dict1 = {'new': 'N', 'old': 'O'}

# # hell(**dict1)
# # hell(dict1.new, dict1.old)
# from django.core.mail import send_mail
# from django.conf import settings
# import random


# def register_user():
#     try:
#         send_mail(
#             subject="Test Subject",
#             message="Test Message",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[settings.RECIPIENT_ADDRESS]
#         ) 
#         return("success")
#     except:
#         return("Fail")

# def generateVerificationCode():
#     rndlist = ['0','1','2','3','4','5','6','7','8','9']

#     rnd = ''

#     for _ in range(6):
#         rnd = rnd + random.SystemRandom().choice(rndlist)
    
#     return rnd

# a = generateVerificationCode()
# print(a)

from .models import User
from django.contrib.auth import get_user_model

def testing(pk):
    # UserModel = get_user_model()
    user = User.objects.get(id=pk)
    print(user.email)

testing(1)