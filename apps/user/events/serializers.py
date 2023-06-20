from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_date', 'end_date', 'content')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ('event', 'image')

class EventGetSerializer(serializers.ModelSerializer):
    event_image = ImageSerializer()

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_date', 'end_date', 'content', 'event_image')