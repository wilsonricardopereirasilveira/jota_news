from django.urls import path
from .health_checks import HealthCheckView

urlpatterns = [
    path('health/live/', HealthCheckView.as_view(), name='health-live'),
    path('health/ready/', HealthCheckView.as_view(), name='health-ready'),
    path('health/deep/', HealthCheckView.as_view(), name='health-deep'),
]
