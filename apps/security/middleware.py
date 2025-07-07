from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_vary_headers


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add basic security-related HTTP headers."""

    def process_response(self, request, response):
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('X-Frame-Options', 'DENY')
        patch_vary_headers(response, ['Cookie'])
        return response
