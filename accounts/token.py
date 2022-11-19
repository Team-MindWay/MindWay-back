import datetime, jwt
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions

from MindWay.settings import SECRET_KEY

JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

def generate_token(payload, type):
    if type is "access":
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    elif type is "refresh":
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    else :
        raise Exception('Invalid Tokentype')

    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    payload['type'] = type
    token = JWT_ENCODE_HANDLER(payload)

    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('uauthenticated')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        return {'user_id' : payload['user_id'], 'username' : payload['username']}
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')