import time
import logging
from django.utils.deprecation import MiddlewareMixin

metric_logger = logging.getLogger('metrics')


class RequestMetricsMiddleware(MiddlewareMixin):
    """Capture request metrics."""

    def process_request(self, request):
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        duration = time.monotonic() - getattr(request, '_start_time', time.monotonic())
        metric_logger.info({
            'metric': 'api.requests.by_endpoint',
            'path': request.path,
            'method': request.method,
            'status': response.status_code,
            'duration_ms': int(duration * 1000),
        })
        return response
