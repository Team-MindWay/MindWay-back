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
        event = Event.objects.first()

        if event is None:
            return Response({'message' : '현재 진행중인 이벤트가 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

        serializer = EventGetSerializer(event)

        return Response(serializer.data)

    def post(self, request):
        admin_valid(request)
        serializer = EventSerializer(data=request.data)
        
        if not serializer.is_valid(raise_exception=True):
            return Response({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        event = Event.objects.first()
        return Response({'message' : 'Success', 'id' : event.id})

    def put(self, request):
        admin_valid(request)
        event = Event.objects.get(id=request.data['id'])
        serializer = EventSerializer(event, data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'message' : 'Success'})

    def delete(self, request):
        admin_valid(request)
        event = Event.objects.get(id=request.data['id'])
        event.delete()

        return Response({'message' : 'Success'})
    
class ImageView(APIView):
    def post(self, request):
        admin_valid(request)
        
        data = {'event' : request.data['id'], 'image' : request.FILES.get('image')}
        serializer = EventImageSerializer(data=data)

        if not serializer.is_valid(raise_exception=True):
            return Response({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message' : 'Success'})