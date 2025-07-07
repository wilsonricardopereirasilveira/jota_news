"""
URL configuration for jota_news project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Views de teste inline
@csrf_exempt
def test_news_direct(request):
    """Endpoint simples para testar notícias"""
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings.development')
    django.setup()

    from apps.news.models import News

    news_list = []
    for news in News.objects.all().select_related('category').prefetch_related('tags'):
        news_data = {
            'id': news.id,
            'title': news.title,
            'content': news.content[:100] + '...',
            'source': news.source,
            'category': news.category.name if news.category else None,
            'is_urgent': news.is_urgent,
            'tags': [tag.name for tag in news.tags.all()[:3]]
        }
        news_list.append(news_data)

    return JsonResponse({
        'status': 'success',
        'count': len(news_list),
        'results': news_list
    })

@csrf_exempt
def test_urgent_direct(request):
    """Endpoint para notícias urgentes"""
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings.development')
    django.setup()

    from apps.news.models import News

    urgent_news = []
    for news in News.objects.filter(is_urgent=True).select_related('category'):
        news_data = {
            'id': news.id,
            'title': news.title,
            'is_urgent': news.is_urgent,
            'category': news.category.name if news.category else None
        }
        urgent_news.append(news_data)

    return JsonResponse({
        'status': 'success',
        'count': len(urgent_news),
        'urgent_news': urgent_news
    })

@csrf_exempt
def test_categories_direct(request):
    """Endpoint para categorias"""
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings.development')
    django.setup()

    from apps.categories.models import Category

    categories = []
    for cat in Category.objects.all():
        news_count = cat.news.count()
        categories.append({
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'news_count': news_count
        })

    return JsonResponse({
        'status': 'success',
        'count': len(categories),
        'categories': categories
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/webhook/", include("apps.webhook.urls")),
    path("", include("apps.monitoring.urls")),
    path("api/", include("apps.api.urls")),
    # URLs de teste simples
    path("test/news/", test_news_direct, name='test-news'),
    path("test/urgent/", test_urgent_direct, name='test-urgent'), 
    path("test/categories/", test_categories_direct, name='test-categories'),
]
