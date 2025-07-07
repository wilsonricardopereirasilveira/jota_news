from rest_framework import serializers


class NewsWebhookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    source = serializers.CharField(max_length=255)
    published_at = serializers.DateTimeField()
    url = serializers.URLField()
    author = serializers.CharField(max_length=100, allow_blank=True, required=False)
