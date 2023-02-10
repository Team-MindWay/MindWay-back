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

# Create your views here.
class AdminEventView(APIView):
    def get(self, request):
        admin_valid(request)
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)

        return Response(serializer.data)

    def post(self, request):
        admin_valid(request)
        serializer = EventSerializer(data=request.data)
        
        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return JsonResponse({'message' : 'Success'})

    def put(self, request):
        admin_valid(request)
        event = Event.objects.get(id=request.data['id'])
        serializer = EventSerializer(event, data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return JsonResponse({'message' : 'Success'})

    def delete(self, request):
        admin_valid(request)
        event = Event.objects.get(id=request.data['id'])
        event.delete()

        return JsonResponse({'message' : 'Success'})