from rest_framework import serializers

from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'user', 'title', 'author', 'url')

class MemberSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()

    class Meta:
        model = TeamMember
        fields = ('team', 'student')

class LibrarySerializer(serializers.ModelSerializer):
    student = MemberSerializer(many=True, required=False)

    class Meta:
        model = Library
        fields = ('id', 'team', 'room', 'student')