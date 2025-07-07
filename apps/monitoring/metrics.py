"""Simple utilities for emitting custom metrics."""
import logging

metrics_logger = logging.getLogger('metrics')


def increment(metric_name: str, value: int = 1, **labels):
    """Log a counter metric."""
    metrics_logger.info({'metric': metric_name, 'value': value, **labels})
