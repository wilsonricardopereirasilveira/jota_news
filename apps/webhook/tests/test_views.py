from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.conf import settings
from unittest.mock import patch


class WebhookNewsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        settings.WEBHOOK_API_KEY = 'secret'
        self.url = reverse('webhook-news')
        self.payload = {
            'title': 'Test',
            'content': 'Something',
            'source': 'Unit',
            'published_at': '2024-01-01T00:00:00Z',
            'url': 'https://example.com',
            'author': 'tester'
        }

    def test_auth_required(self):
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_valid_post(self):
        self.client.credentials(HTTP_X_API_KEY='secret')
        with patch('apps.webhook.services.SQSService.send_message') as mock_send:
            response = self.client.post(self.url, self.payload, format='json')
            self.assertEqual(response.status_code, 201)
            mock_send.assert_called_once()
