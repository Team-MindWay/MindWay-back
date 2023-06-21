import boto3
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

        serializer = EventSerializer(event)

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
    
def upload_file_to_s3(file):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    try:
        s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file.name)
        return True
    except Exception as e:
        logging.info(e)
        return False

class ImageS3UploadView(APIView):
    def post(self, request):
        admin_valid(request)

        image = request.FILES.get('image')
        upload_status = upload_file_to_s3(image)

        if not upload_status:
            return Response({'message' : 'S3 Upload Fail'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'ImageUrl' : f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{image.name}'})