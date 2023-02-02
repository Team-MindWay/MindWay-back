from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from .models import User

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

def authenticate(email, password):
    try:
        user = User.objects.get(email=email)

        if user.password == password:
            return user
    except User.DoesNotExist:
        return None