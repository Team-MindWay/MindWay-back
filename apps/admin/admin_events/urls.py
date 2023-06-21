from django.urls import path
from .views import *

urlpatterns = [
    path('', AdminEventView.as_view()),
    path('/image', ImageS3UploadView.as_view())
]