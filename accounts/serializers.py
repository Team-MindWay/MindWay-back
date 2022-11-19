from rest_framework import serializers

from .models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
        )

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        user = User.objects.get(email=email)

        if user is None:
            return {'email' : None}

        return {'id' : user.id, 'email' : user.email, 'is_active' : user.is_active}

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'password',
        )