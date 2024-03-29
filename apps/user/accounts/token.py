import datetime, jwt
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed

from .models import User

JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

def generate_token(payload, type):
    if type == "access":
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    elif type == "refresh":
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=4)
    else :
        raise Exception('Invalid Tokentype')

    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    payload['type'] = type
    token = JWT_ENCODE_HANDLER(payload)

    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('uauthenticated')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

        return {'user_id' : payload['user_id'], 'username' : payload['username']}
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

def get_exp(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        exp = datetime.datetime.fromtimestamp(payload['exp'])

        return exp
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

def user_valid(request):
    try:
        auth = request.META.get('HTTP_AUTHORIZATION').split()

        if auth and len(auth) == 2:
            id = decode_access_token(auth[1])
            user = User.objects.get(id=id)

            return user
        raise AuthenticationFailed('unauthenticated')
    except:
        raise AuthenticationFailed('unauthenticated')

def admin_valid(request):
    try:
        auth = request.META.get('HTTP_AUTHORIZATION').split()

        if auth and len(auth) == 2:
            id = decode_access_token(auth[1])
            user = User.objects.get(id=id)

            if user.is_superuser == True:
                return user
        raise AuthenticationFailed('unauthenticated')
    except:
        raise AuthenticationFailed('unauthenticated')