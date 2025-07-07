from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuth(JWTAuthentication):
    """Wrapper around Simple JWT authentication."""
    pass


class WebhookAPIKeyAuth(BaseAuthentication):
    """Simple API key authentication for webhooks."""

    def authenticate(self, request):
        token = request.headers.get('X-API-Key')
        expected = getattr(settings, 'WEBHOOK_API_KEY', None)
        if not expected or token != expected:
            raise exceptions.AuthenticationFailed('Invalid token')
        return (None, None)
