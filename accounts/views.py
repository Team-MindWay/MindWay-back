import jwt
from rest_framework import generics, status
from django.http import JsonResponse

from .serializers import SignupSerializer

import logging
import logging.config
from MindWay.settings import DEFAULT_LOGGING

logging.config.dictConfig(DEFAULT_LOGGING)

# Create your views here.
class Signup(generics.GenericAPIView):
    def post(self, request):
        userdata = request.data

        serializer = SignupSerializer(data=userdata)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)