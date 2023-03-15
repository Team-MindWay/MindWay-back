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