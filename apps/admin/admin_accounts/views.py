import jwt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache

from .serializer import *
from .models import *
from apps.user.accounts.serializers import *

class AdminLogin(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid()
        user = serializer.validated_data

        if user['id'] is None:
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_401_UNAUTHORIZED)

        if user['is_superuser'] == False:
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_403_FORBIDDEN)

        try :
            token = Refresh.objects.get(id=user['id'])

            if token:
                data = {'user' : user['id'], 'refresh' : user['refresh_token']}
                refresh = TokenSerializer(token, data=data)
    
                if not refresh.is_valid(raise_exception=True):
                    return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)
    
                refresh.save()
        except:
            data = {'user' : user['id'], 'refresh' : user['refresh_token']}
            refresh = TokenSerializer(data=data)

            if not refresh.is_valid(raise_exception=True):
                return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)

            refresh.save()
        return JsonResponse({'access_token' : user['access_token'], 'refresh_token' : user['refresh_token']})