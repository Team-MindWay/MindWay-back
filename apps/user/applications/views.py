from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.accounts.token import user_valid
from apps.user.accounts.models import User
from .serializers import *
from .models import *

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

# Create your views here.
class BookApplication(APIView):
    def get(self, request):
        user_valid(request)
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = user_valid(request)
        request.data._mutable = True
        request.data['user'] = user.id
        serializer = BookSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})

    def put(self, request):
        user = user_valid(request)
        book = Book.objects.get(pk=request.data['id'])

        if not user == book.user:
            return JsonResponse({'message' : '본인이 신청한 책만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        request.data._mutable = True
        request.data['user'] = user.id

        serializer = BookSerializer(book, data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return JsonResponse({'message' : 'Success'})
    
    def delete(self, request):
        user = user_valid(request)
        book = Book.objects.get(pk=request.data['id'])

        if not user == book.user:
            return JsonResponse({'message' : '본인이 신청한 책만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        book.delete()

        return JsonResponse({'message' : 'Success'})

class BookInfo(APIView):
    def get(self, request, id):
        user_valid(request)

        book = Book.objects.get(pk=id)
        serializer = BookSerializer(book)

        return Response(serializer.data)

class LibraryApplication(APIView):
    def get(self, request):
        user_valid(request)

        team = Library.objects.prefetch_related('student').all()
        serializer = LibrarySerializer(team, many=True)

        return Response(serializer.data)

    def post(self, request):
        user_valid(request)
        request.data._mutable = True
        member_list = request.data.pop('member')

        library_serializer = LibrarySerializer(data=request.data)
        
        if not library_serializer.is_valid(raise_exception=True):
            return JsonResponse({'message' : 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        library_serializer.save()
        
        team = Library.objects.filter(team=request.data['team']).first()

        for member in member_list:
            info = member.split(' ')
            user = User.objects.get(number=info[0], username=info[1])
            data = {'team' : team.pk, 'student' : user.id}
            member_serializer = MemberSerializer(data=data)

            if not member_serializer.is_valid(raise_exception=True):
                return JsonResponse({'message' : 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

            member_serializer.save()

        return JsonResponse({'message' : 'Success'})

    def delete(self, request):
        user = user_valid(request)
        library = Library.objects.get(pk=request.data['id'])
        member = TeamMember.objects.filter(team=library).values_list('student', flat=True)

        if not user.id in member:
            return JsonResponse({'message' : f'{library.team}의 팀원이 아닙니다.'}, status=status.HTTP_403_FORBIDDEN)

        library.delete()

        return JsonResponse({'message' : 'Success'})