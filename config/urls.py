"""
URL Configuration for Ministry of Health IT Operations Management System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/assets/', include('apps.assets.urls')),
    path('api/tickets/', include('apps.helpdesk.urls')),
    path('api/visitors/', include('apps.visitors.urls')),
    path('api/network/', include('apps.network.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/backup/', include('apps.backup.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
