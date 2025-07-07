from django.db import models
from .models import News


def get_news_optimized(category=None, limit=20):
    queryset = News.objects.select_related('category', 'subcategory')
    queryset = queryset.prefetch_related('tags')
    if category:
        queryset = queryset.filter(category__slug=category)
    return queryset[:limit]

