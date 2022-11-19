from django.urls import path
from .views import *

urlpatterns = [
    path('signup', Signup.as_view()),
    path('validation/<str:uid>/<str:token>', Validation.as_view()),
    path('request/validation', RequestValidation.as_view()),
    path('password/change', ChangePassword.as_view()),
    path('login', Login.as_view()),
    path('info', UserInfo.as_view()),
]