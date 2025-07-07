from rest_framework.views import APIView
from rest_framework.response import Response
from apps.news.models import News, Tag
from apps.categories.models import Category


class StatsView(APIView):
    def get(self, request):
        return Response({
            'news_count': News.objects.count(),
            'urgent_news': News.objects.filter(is_urgent=True).count(),
            'categories': Category.objects.count(),
            'tags': Tag.objects.count(),
        })
