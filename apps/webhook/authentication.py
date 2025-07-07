from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('X-API-Key')
        expected = getattr(settings, 'WEBHOOK_API_KEY', None)
        if not expected or token != expected:
            raise exceptions.AuthenticationFailed('Invalid token')
        return (None, None)
