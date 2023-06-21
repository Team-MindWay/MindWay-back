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

# Create your views here.
class EventInfo(APIView):
    def get(self, request):
        user_valid(request)
        event = Event.objects.first()

        if event is None:
            return JsonResponse({'message' : '현재 진행중인 이벤트가 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

        serializer = EventSerializer(event)

        return Response(serializer.data)