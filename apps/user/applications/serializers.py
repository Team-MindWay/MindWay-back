from rest_framework import serializers

from apps.user.accounts.serializers import UserSerializer
from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'user', 'title', 'author', 'url')

class MemberSerializer(serializers.ModelSerializer):
    student = UserSerializer(many=False, required=False)

    class Meta:
        model = TeamMember
        fields = ('team', 'student')

class LibrarySerializer(serializers.ModelSerializer):
    student = MemberSerializer(many=True, required=False)

    class Meta:
        model = Library
        fields = ('id', 'team', 'room', 'student')

class MemberUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('team', 'student')