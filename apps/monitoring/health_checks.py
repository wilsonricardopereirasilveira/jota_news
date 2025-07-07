from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import connection
from django.conf import settings
import boto3
import logging

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def check_database(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except Exception as exc:
            logger.error({'db_error': str(exc)})
            return False

    def check_sqs(self):
        try:
            client = boto3.client(
                'sqs',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            client.list_queues(MaxResults=1)
            return True
        except Exception as exc:
            logger.error({'sqs_error': str(exc)})
            return False

    def check_lambda(self):
        try:
            client = boto3.client(
                'lambda',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            client.list_functions(MaxItems=1)
            return True
        except Exception as exc:
            logger.error({'lambda_error': str(exc)})
            return False

    def get(self, request):
        checks = {
            'database': self.check_database(),
            'sqs': self.check_sqs(),
            'lambda': self.check_lambda(),
            'timestamp': timezone.now(),
        }
        status_code = status.HTTP_200_OK if all(checks.values()) else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(checks, status=status_code)
