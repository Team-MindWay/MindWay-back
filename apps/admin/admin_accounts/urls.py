from django.urls import path
from .views import *

urlpatterns = [
    path('login', AdminLogin.as_view()),
    path('refresh', AdminRefresh.as_view()),
]