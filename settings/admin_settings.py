from .user_settings import *

INSTALLED_APPS += [
    'apps.admin.admin_accounts',
    'apps.admin.admin_applications',
]
ROOT_URLCONF = 'MindWay.urls_admin'