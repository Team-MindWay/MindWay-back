import bcrypt
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from .models import User

import logging
import logging.config

logging.config.dictConfig(settings.DEFAULT_LOGGING)

def authenticate(email, password):
    try:
        user = User.objects.get(email=email)

        hashedpw = user.password.encode('utf-8')
        password = password.encode('utf-8')

        if bcrypt.checkpw(password, hashedpw):
            return user
    except User.DoesNotExist:
        return None