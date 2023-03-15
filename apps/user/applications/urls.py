from django.urls import path
from .views import *

urlpatterns = [
    path('book', BookApplication.as_view()),
    path('book/info/<int:id>', BookInfo.as_view()),
    path('recommend', BookRecommend.as_view()),
]