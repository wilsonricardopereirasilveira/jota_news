from datetime import timedelta
import logging
from celery import shared_task
from django.utils import timezone
from django.db.models import Count

from .models import News

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_news():
    """Remove notícias antigas (> 1 ano)"""
    cutoff_date = timezone.now() - timedelta(days=365)
    count, _ = News.objects.filter(published_at__lt=cutoff_date).delete()
    logger.info("Removed %s old news articles", count)


@shared_task
def generate_daily_report():
    """Gera relatório diário de notícias"""
    today = timezone.now().date()
    stats = {
        'total_news': News.objects.filter(created_at__date=today).count(),
        'by_category': list(
            News.objects.filter(created_at__date=today)
                .values('category__name')
                .annotate(count=Count('id'))
        )
    }
    logger.info("Daily report: %s", stats)

