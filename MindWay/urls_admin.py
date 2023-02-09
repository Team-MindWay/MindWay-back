from .urls import *

urlpatterns += [
    path("accounts/", include('apps.admin.admin_accounts.urls')),
    path('applications/', include('apps.admin.admin_applications.urls')),
    path('events/', include('apps.admin.admin_events.urls')),
]