from django.urls import path
from .views import *

urlpatterns = [
    path('signup', Signup.as_view()),
    path('validation/<str:uid>/<str:token>', Validation.as_view()),
]