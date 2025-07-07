from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.categories.models import Category, Subcategory
from apps.news.models import News, Tag
from ..serializers.category_serializers import CategorySerializer, CategoryDetailSerializer, SubcategorySerializer
from ..serializers.news_serializers import NewsSerializer
from ..serializers.tag_serializers import TagSerializer
from ..permissions.editorial_permissions import IsEditorOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsEditorOrReadOnly]

    @action(detail=True, methods=['get'], url_path='news')
    def news(self, request, pk=None):
        category = self.get_object()
        qs = category.news.all().select_related('category', 'subcategory').prefetch_related('tags')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = NewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = NewsSerializer(qs, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsEditorOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsEditorOrReadOnly]

    @action(detail=True, methods=['get'], url_path='news')
    def news(self, request, pk=None):
        tag = self.get_object()
        qs = tag.news.all().select_related('category', 'subcategory').prefetch_related('tags')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = NewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = NewsSerializer(qs, many=True)
        return Response(serializer.data)
