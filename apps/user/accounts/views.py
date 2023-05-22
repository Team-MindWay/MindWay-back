import jwt
import bcrypt
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect

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
        userdata = request.data.copy()
        
        if not userdata['password'] == userdata['password_check']:
            return JsonResponse({'message' : '비밀번호 확인에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        password = userdata['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        data = {
            'email' : userdata['email'],
            'number' : userdata['number'],
            'username' : userdata['username'],
            'password' : hashed_password.decode('utf-8')
        }

        serializer = SignupSerializer(data=data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        send(request, userdata['email'], 'signup')

        return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)

class Validation(generics.GenericAPIView):
    def get(self, request, uid, token):
        try :
            token_data = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(email=token_data['email'])
            
            if not user.email == token_data['email']:
                return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            cache_data = cache.get(user.email)

            if token_data['type'] == 'signup':
                if cache_data is None:
                    if user.is_active == False:
                        user.delete()
                        
                        return redirect('http://localhost:3000/signup/expire')
                    elif user.is_active == True:
                        return redirect('http://localhost:3000/email/error')
                    
                if uid == str(cache_data):
                    user.is_active = True
                    user.save()
                    cache.delete(user.email)

                    return redirect('http://localhost:3000/signup/success')
                else :
                    return redirect('http://localhost:3000/email/error')
            elif token_data['type'] == 'password':
                if cache_data is None:
                    return redirect('http://localhost:3000/password/update/expire')

                if uid == str(cache_data):
                    cache.set(user.email, 'True', 30)

                    return redirect('http://localhost:3000/password/update/success')
                else :
                    return redirect('http://localhost:3000/email/error')
        except ValidationError:
            return JsonResponse({'message' : 'Type Error'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return redirect('http://localhost:3000/email/error')

class RequestValidation(generics.GenericAPIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user['email'] == None:
            return JsonResponse({'message' : '가입되지 않은 이메일입니다.'}, status=status.HTTP_403_FORBIDDEN)

        if user['is_active'] == False:
            return JsonResponse({'message' : '인증되지 않은 사용자입니다. 메일을 확인해주세요.'}, status=status.HTTP_403_FORBIDDEN)

        send(request, user['email'], 'password')
        
        return JsonResponse({'message' : 'Success'})

class ChangePassword(generics.GenericAPIView):
    def put(self, request):
        email = request.data['email']
        cache_data = cache.get(email)

        if cache_data != 'True' or cache_data is None:
            return JsonResponse({'message' : '인증되지 않은 사용자입니다. 메일을 확인해주세요.'}, status=status.HTTP_403_FORBIDDEN)

        password = request.data['password']

        if not password == request.data['password_check']:
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        encoded_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
        serializer = ChangePasswordSerializer(user, data={'password' : hashed_password.decode('utf-8')})

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        cache.delete(email)

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
            return JsonResponse({'message' : '가입되지 않은 사용자입니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        if user['password'] == False:
            return JsonResponse({'message' : '잘못된 비밀번호입니다.'}, status=status.HTTP_403_FORBIDDEN)

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
        exp = get_exp(user['access_token'])
        return JsonResponse({'access_token' : user['access_token'], 'refresh_token' : user['refresh_token'], 'expire' : exp})

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
        exp = get_exp(token['access_token'])
        return JsonResponse({'access_token' : token['access_token'], 'refresh_token' : token['refresh_token'], 'expire' : exp})

class Logout(generics.GenericAPIView):
    def put(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()

        if auth and len(auth) == 2:
            id = decode_access_token(auth[1])
            user = User.objects.get(id=id)
            token = Refresh.objects.get(user=user.id)

            token.delete()
        
        return JsonResponse({'message' : 'Success'})