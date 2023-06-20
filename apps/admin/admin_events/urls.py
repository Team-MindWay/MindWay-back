from django.urls import path
from .views import *

urlpatterns = [
    path('', AdminEventView.as_view()),
    path('/image', ImageView.as_view()),
]