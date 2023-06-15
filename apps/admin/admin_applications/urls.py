from django.urls import path
from .views import *

urlpatterns = [
    path('book', AdminBookApplication.as_view()),
    path('recommend', AdminBookRecommend.as_view()),
    path('recommend/info/<int:id>', AdminBookRecommendInfo.as_view())
]