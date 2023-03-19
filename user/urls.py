from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('getUserPhoto/', views.get_user_photo, name="get_user_photo"),
    path('login/', views.signin, name="signin"),
    path('logout/', views.signout, name="signout"),
    path('signup/', views.signup, name="signup"),
    path('sendVerificationCode/', views.send_verification_code, name="register"),
    path('receive_verification_code/', views.receive_verification_code, name="receive_verification_code"),
    path('changePassword/', views.changePassword, name="changePassword"),
] 
if settings.DEBUG:
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



