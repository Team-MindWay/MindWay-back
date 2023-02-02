from django.urls import path
from .views import *

urlpatterns = [
    path('', EventInfo.as_view()),
]