from .urls import *

urlpatterns += [
    path("accounts/", include('apps.user.accounts.urls')),
    path("applications/", include('apps.user.applications.urls')),
]