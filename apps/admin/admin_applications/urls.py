from django.urls import path
from .views import *

urlpatterns = [
    path('library', AdminLibraryApplication.as_view()),
    path('book', AdminBookApplication.as_view()),
]