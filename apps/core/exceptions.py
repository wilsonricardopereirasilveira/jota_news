class WebhookException(Exception):
    """Base exception for webhook errors."""

class AuthenticationFailed(WebhookException):
    pass

class RateLimitExceeded(WebhookException):
    pass

