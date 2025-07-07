import time
from collections import defaultdict
from django.http import JsonResponse
from .exceptions import RateLimitExceeded


class RateLimitMiddleware:
    """Simple rate limiting per IP."""

    def __init__(self, get_response, max_requests=100, window=60):
        self.get_response = get_response
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        now = time.time()
        timestamps = self.requests[ip]
        timestamps = [ts for ts in timestamps if now - ts < self.window]
        timestamps.append(now)
        self.requests[ip] = timestamps
        if len(timestamps) > self.max_requests:
            return JsonResponse({'detail': 'rate limit exceeded'}, status=429)
        return self.get_response(request)
