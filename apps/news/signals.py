from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from .models import News


@receiver(post_save, sender=News)
def invalidate_news_cache(sender, instance, **kwargs):
    cache_keys = [
        f'news_category_{instance.category.slug}',
        'news_latest',
        'news_urgent'
    ]
    cache.delete_many(cache_keys)

