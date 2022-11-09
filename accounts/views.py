import jwt
from rest_framework import generics, status
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.core.exceptions import ValidationError
from django.conf import settings

from .serializers import SignupSerializer
from .models import *
from .email import send

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

# Create your views here.
class Signup(generics.GenericAPIView):
    def post(self, request):
        userdata = request.data

        serializer = SignupSerializer(data=userdata)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        send(request, userdata['email'])

        return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)

class Validation(generics.GenericAPIView):
    def get(self, request, uid, token):
        try :
            decode_uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(email=decode_uid)
            user_email = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

            if not user.email == user_email['email']:
                return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()

            return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse({'message' : 'Type Error'}, status=status.HTTP_400_BAD_REQUEST)