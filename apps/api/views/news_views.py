from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.news.models import News, Tag
from apps.categories.models import Category, Subcategory
from ..serializers.news_serializers import NewsSerializer, NewsCreateUpdateSerializer
from ..filters.news_filters import NewsFilter
from ..permissions.editorial_permissions import IsEditorOrReadOnly


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().select_related('category', 'subcategory').prefetch_related('tags')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['title', 'content']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']
    permission_classes = [IsEditorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NewsCreateUpdateSerializer
        return NewsSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], url_path='mark-urgent')
    def mark_urgent(self, request, pk=None):
        news = self.get_object()
        news.is_urgent = True
        news.save()
        serializer = self.get_serializer(news)
        return Response(serializer.data)
