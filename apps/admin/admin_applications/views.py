from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.accounts.token import admin_valid
from .serializers import *
from .models import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

class AdminBookApplication(APIView):
    def get(self, request):
        admin_valid(request)
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        return Response(serializer.data)
    
    def delete(self, request):
        admin_valid(request)
        book = Book.objects.get(pk=request.data['id'])
        book.delete()

        return JsonResponse({'message' : 'Success'})
    
class AdminBookRecommend(APIView):
    def get(self, request):
        admin_valid(request)
        data = Recommend.objects.all()
        serializer = RecommendInfoSerializer(data, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = admin_valid(request)
        request_data = request.data
        data = {
            'title' : request_data['title'],
            'author' : request_data['author'],
            'recommender' : user.id,
            'outline' : request_data['outline'],
            'category' : request_data['category']
        }
        serializer = RecommendSerializer(data=data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})
    
    def put(self, request):
        user = admin_valid(request)
        recommend = Recommend.objects.get(pk=request.data['id'])
        request_data = request.data

        if not user == recommend.recommender:
            return JsonResponse({'message' : '본인이 신청한 도서만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = {
            'title' : request_data['title'],
            'author' : request_data['author'],
            'recommender' : user.id,
            'outline' : request_data['outline'],
            'category' : request_data['category']
        }

        serializer = RecommendSerializer(recommend, data=data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})

    def delete(self, request):
        user = admin_valid(request)
        recommend = Recommend.objects.get(id=request.data['id'])

        if not user == recommend.recommender:
            return JsonResponse({'message' : '본인이 신청한 도서만 삭제할 수 있습니다.'})
        
        recommend.delete()

        return JsonResponse({'message' : 'Success'})
    
class AdminBookRecommendInfo(APIView):
    def get(self, request, id):
        admin_valid(request)
        recommend = Recommend.objects.get(id=id)

        recommend_serializer = RecommendInfoSerializer(recommend)
        
        return Response(recommend_serializer.data)