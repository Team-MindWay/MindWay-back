import jwt
import bcrypt
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.conf import settings
from django.core.cache import cache

from .serializers import *
from .models import *
from .email import send
from .token import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

# Create your views here.
class Signup(APIView):
    def post(self, request):
        userdata = request.data
        userdata._mutable = True
        
        if not userdata['password'] == userdata['password_check']:
            return JsonResponse({'message' : '비밀번호 확인에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        password = userdata['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        logging.info(hashed_password)
        userdata['password'] = hashed_password

        serializer = SignupSerializer(data=userdata)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        send(request, userdata['email'], 'signup')

        return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)

class Validation(generics.GenericAPIView):
    def get(self, request, uid, token):
        try :
            decode_uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(email=decode_uid)
            user_email = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

            if not user.email == user_email['email']:
                return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_active is True:
                cache_data = cache.get(user.email)
                if cache_data == 'False':
                    cache.set(user.email, 'True', 30)

                return JsonResponse({'message' : 'success'}) ## redirect front url(change_password page)

            user.is_active = True
            user.save()

            return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK) ## render template(signup success)
        except ValidationError:
            return JsonResponse({'message' : 'Type Error'}, status=status.HTTP_400_BAD_REQUEST)

class RequestValidation(generics.GenericAPIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user['email'] == None:
            return JsonResponse({'message' : '가입되지 않은 이메일입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user['is_active'] == False:
            return JsonResponse({'message' : '인증되지 않은 사용자입니다. 메일을 확인해주세요.'}, status=status.HTTP_403_FORBIDDEN)

        send(request, user['email'], 'password')
        request.session['email'] = user['email']

        if not cache.get(user['email']):
            cache.set(user['email'], 'False', 30)
        
        return JsonResponse({'message' : 'Success'})

class ChangePassword(generics.GenericAPIView):
    def put(self, request):
        cache_data = cache.get(request.session['email'])

        if cache_data == 'False' or cache_data is None:
            return JsonResponse({'message' : '인증되지 않은 사용자입니다. 메일을 확인해주세요.'}, status=status.HTTP_401_UNAUTHORIZED)

        password = request.data['password']

        if not password == request.data['password_check']:
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=request.session['email'])
        serializer = ChangePasswordSerializer(user, data={'password' : password})

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        cache.delete(request.session['email'])
        del request.session['email']

        return JsonResponse({'message' : 'Success'})

class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user['id'] is None:
            return JsonResponse({'message' : '가입되지 않은 사용자입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user['is_active'] == False:
            return JsonResponse({'message' : '인증되지 않은 사용자입니다. 메일을 확인해주세요.'}, status=status.HTTP_403_FORBIDDEN)

        try :
            token = Refresh.objects.get(user=user['id'])

            if token:
                refresh = TokenSerializer(
                    token,
                    data = {
                        'user' : user['id'],
                        'refresh' : user['refresh_token'],
                    }
                )
    
                if not refresh.is_valid(raise_exception=True):
                    return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
    
                refresh.save()
        except:
            refresh = TokenSerializer(
                data = {
                    'user' : user['id'],
                    'refresh' : user['refresh_token'],
                }
            )

            if not refresh.is_valid(raise_exception=True):
                return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            refresh.save()
        return JsonResponse({'access_token' : user['access_token'], 'refresh_token' : user['refresh_token']})

class UserInfo(generics.GenericAPIView):
    def get(self, request):
        user = user_valid(request)
        serializer = UserSerializer(user)

        return Response(serializer.data)

class UserRefresh(generics.GenericAPIView):
    serializer_class = RefreshSerializer

    def patch(self, request):
        refresh = request.data['refresh_token']
        user = decode_refresh_token(refresh)
        pre_token = Refresh.objects.get(user=user['user_id'])

        if not pre_token.refresh == refresh:
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RefreshSerializer(data={'id' : user['user_id']})

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data

        update_token = TokenSerializer(
            pre_token,
            data = {
                'user' : user['user_id'],
                'refresh' : token['refresh_token']
            }
        )

        if not update_token.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        update_token.save()

        return JsonResponse({'access_token' : token['access_token'], 'refresh_token' : token['refresh_token']})

class Logout(generics.GenericAPIView):
    def put(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()

        if auth and len(auth) == 2:
            id = decode_access_token(auth[1])
            user = User.objects.get(id=id)
            token = Refresh.objects.get(user=user.id)

            token.delete()
        
        return JsonResponse({'message' : 'Success'})