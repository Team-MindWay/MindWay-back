from .base import *

INSTALLED_APPS += [
    'apps.admin.admin_accounts',
    'apps.user.accounts',
]
ROOT_URLCONF = 'MindWay.urls_admin'