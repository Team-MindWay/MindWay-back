from .urls import *

urlpatterns += [
    path("accounts/", include('apps.admin.admin_accounts.urls')),
]