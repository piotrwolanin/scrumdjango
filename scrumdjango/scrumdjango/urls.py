from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scrumboard.urls')),
    path('backlog/', include('backlog.urls')),
    path('accounts/', include('accounts.urls')),
    path('session_security/', include('session_security.urls')),
]