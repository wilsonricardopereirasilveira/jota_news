import logging
from pythonjsonlogger import jsonlogger
try:
    import watchtower
except Exception:  # pragma: no cover - watchtower may not be installed in tests
    watchtower = None


def configure_logging():
    """Configure structured logging to CloudWatch if watchtower is available."""
    logger = logging.getLogger()
    if not logger.handlers:
        handler = None
        if watchtower:
            handler = watchtower.CloudWatchLogHandler(log_group='/aws/ecs/jota-api')
        else:
            handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
