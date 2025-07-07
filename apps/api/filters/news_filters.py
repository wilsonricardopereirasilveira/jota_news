import django_filters
from django.db.models import Q
from apps.news.models import News, Tag


class NewsFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    subcategory = django_filters.CharFilter(field_name='subcategory__slug')
    tags = django_filters.CharFilter(method='filter_tags')
    is_urgent = django_filters.BooleanFilter(field_name='is_urgent')
    published_after = django_filters.DateFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_at', lookup_expr='lte')
    source = django_filters.CharFilter(field_name='source', lookup_expr='iexact')

    class Meta:
        model = News
        fields = []

    def filter_tags(self, queryset, name, value):
        slugs = [t.strip() for t in value.split(',') if t.strip()]
        return queryset.filter(tags__slug__in=slugs).distinct()
