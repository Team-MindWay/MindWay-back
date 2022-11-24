from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.token import user_valid
from .serializers import *
from .models import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

# Create your views here.
class BookApplication(APIView):
    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()
        user_valid(auth)
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()
        user = user_valid(auth)
        request.data._mutable = True
        request.data['user'] = user.id
        serializer = BookSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})

    def put(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()
        user = user_valid(auth)

        book = Book.objects.get(pk=request.data['id'])

        if not user == book.user:
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_403_FORBIDDEN)

        request.data._mutable = True
        request.data['user'] = user.id

        serializer = BookSerializer(book, data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})
    
    def delete(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()
        user = user_valid(auth)

        book = Book.objects.get(pk=request.data['id'])

        if not user == book.user:
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_403_FORBIDDEN)
        
        book.delete()

        return JsonResponse({'message' : 'Success'})