from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.conf import settings

from apps.user.accounts.backends import authenticate
from .models import *
from apps.user.accounts.token import generate_token

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=254)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            return {'id' : None, 'email' : email}

        try :
            payload = JWT_PAYLOAD_HANDLER(user)
            access_token = generate_token(payload, 'access')
            refresh_token = generate_token(payload, 'refresh')
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exist'
            )

        return {'id' : user.id, 'email' : email, 'is_active' : user.is_active, 'is_superuser': user.is_superuser, 'access_token' : access_token, 'refresh_token' : refresh_token}