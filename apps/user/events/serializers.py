from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_date', 'end_date', 'content', 'image')