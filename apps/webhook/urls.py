from django.urls import path
from .views import WebhookNewsView

urlpatterns = [
    path('news/', WebhookNewsView.as_view(), name='webhook-news'),
]
