from .base import *

INSTALLED_APPS += [
    'apps.user.accounts',
    'apps.user.applications',
    'apps.user.events',
]
ROOT_URLCONF = 'MindWay.urls_user'