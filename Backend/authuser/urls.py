from django.urls import path

from .views import AuthUSer

urlpatterns = [
    path('login/', AuthUSer.as_view({'post': 'authUser'}), name='authuser'),
    path('sendotp/', AuthUSer.as_view({'post': 'sendOTP'}), name='sendOTP'),
    path('verifyotp/', AuthUSer.as_view({'post': 'verifyOTP'}), name='verifyOTP'),
    path('resetpassword/', AuthUSer.as_view({'post': 'resetpassword'}), name='resetpassword'),
]
