from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView

from accounts.token import user_valid
from .serializers import *
from .models import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

# Create your views here.
class BookApplication(APIView):
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