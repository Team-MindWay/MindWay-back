from .base import *

INSTALLED_APPS += [
    'apps.user.accounts',
    'apps.user.applications',
]
ROOT_URLCONF = 'MindWay.urls_user'