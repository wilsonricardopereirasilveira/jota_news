from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.categories.models import Category
from apps.news.models import News


class TestNewsAPIIntegration(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Tributos", slug="tributos")
        News.objects.create(
            category=self.category,
            title="Test",
            content="Something",
            source="Unit",
            published_at="2024-01-01T00:00:00Z",
        )

    def test_list_news(self):
        url = reverse("news-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["count"] == 1
