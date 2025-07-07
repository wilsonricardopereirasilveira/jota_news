from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.news.models import News


class NewsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Tributos', slug='tributos')
        User = get_user_model()
        self.user = User.objects.create_user('editor', password='pass', is_staff=True)
        self.news = News.objects.create(
            category=self.category,
            title='Test',
            content='Content',
            source='Unit',
            published_at='2024-01-01T00:00:00Z'
        )

    def test_list_news(self):
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_mark_urgent(self):
        url = reverse('news-mark-urgent', args=[self.news.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)
        self.news.refresh_from_db()
        self.assertTrue(self.news.is_urgent)
