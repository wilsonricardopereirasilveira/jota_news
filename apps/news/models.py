from django.db import models
from apps.categories.models import Category, Subcategory


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    is_urgent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='NewsTag', related_name='news')

    class Meta:
        indexes = [
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['is_urgent', '-created_at']),
            models.Index(fields=['source', '-published_at']),
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title


class NewsTag(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'tag')

    def __str__(self):
        return f"{self.news.title} - {self.tag.name}"
