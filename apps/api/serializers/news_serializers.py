from rest_framework import serializers
from apps.news.models import News, Tag
from apps.categories.models import Category, Subcategory
from lambda_processor.classifier.urgency_scorer import UrgencyScorer

from .category_serializers import CategorySerializer, SubcategorySerializer
from .tag_serializers import TagSerializer


class NewsBaseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    urgency_score = serializers.SerializerMethodField()
    tags_count = serializers.IntegerField(source='tags.count', read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'source', 'published_at',
            'category', 'subcategory', 'tags', 'is_urgent',
            'urgency_score', 'tags_count', 'created_at', 'updated_at'
        ]

    def get_urgency_score(self, obj):
        scorer = UrgencyScorer()
        return scorer.score(obj.title, obj.content, obj.published_at.isoformat())


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    def validate_title(self, value):
        if len(value) > 255:
            raise serializers.ValidationError("Title too long")
        from apps.security.validators import clean_html
        return clean_html(value)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'source', 'published_at',
            'category', 'subcategory', 'tags', 'is_urgent'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        news = News.objects.create(**validated_data)
        if tags:
            news.tags.set(tags)
        return news

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance

class NewsSerializer(NewsBaseSerializer):
    class Meta(NewsBaseSerializer.Meta):
        pass
