"""
URL configuration for jota_news project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/webhook/", include("apps.webhook.urls")),
    path("", include("apps.monitoring.urls")),
    path("api/", include("apps.api.urls")),
]
