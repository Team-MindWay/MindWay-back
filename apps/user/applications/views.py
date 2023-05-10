from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.accounts.token import user_valid
from apps.user.accounts.models import User
from .serializers import *
from .models import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

# Create your views here.
class BookApplication(APIView):
    def get(self, request):
        user_valid(request)
        queryset = Book.objects.all()
        serializer = BookInfoSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = user_valid(request)
        request_data = request.data
        data = {
            'user' : user.id,
            'title' : request_data['title'],
            'author' : request_data['author'],
            'url' : request_data['url']
        }
        serializer = BookSerializer(data=data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})

    def put(self, request):
        user = user_valid(request)
        book = Book.objects.get(pk=request.data['id'])
        request_data = request.data

        if not user == book.user:
            return JsonResponse({'message' : '본인이 신청한 책만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        data = {
            'user' : user.id,
            'title' : request_data['title'],
            'author' : request_data['author'],
            'url' : request_data['url']
        }

        serializer = BookSerializer(book, data=data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})
    
    def delete(self, request):
        user = user_valid(request)
        book = Book.objects.get(pk=request.data['id'])

        if not user == book.user:
            return JsonResponse({'message' : '본인이 신청한 책만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        book.delete()

        return JsonResponse({'message' : 'Success'})

class BookInfo(APIView):
    def get(self, request, id):
        user_valid(request)

        book = Book.objects.get(pk=id)
        serializer = BookInfoSerializer(book)

        return Response(serializer.data)
    
class BookRecommend(APIView):
    def get(self, request):
        user_valid(request)

        data = Recommend.objects.all()
        serializer = RecommendInfoSerializer(data, many=True)

        return Response(serializer.data)