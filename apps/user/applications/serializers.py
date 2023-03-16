from rest_framework import serializers

from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'user', 'title', 'author', 'url')

class RecommendSerializer(serializers.ModelSerializer):
    recommender = serializers.SerializerMethodField()

    class Meta:
        model = Recommend
        fields = ('id', 'recommender', 'title', 'author', 'outline')

    def get_recommender(self, obj):
        return {'id' : obj.recommender.id, 'number' : obj.recommender.number, 'username' : obj.recommender.username}