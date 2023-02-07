from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.accounts.token import user_valid
from .serializers import *
from .models import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

class AdminLibraryApplication(APIView):
    def get(self, request):
        user_valid(request)
        book = Book.objects.all()
        serializer = LibrarySerializer(book, many=True)

        return Response(serializer.data)
