import boto3
import json
from django.conf import settings
from botocore.exceptions import ClientError
from apps.core.utils import logger


class SQSService:
    def __init__(self):
        self.client = boto3.client(
            'sqs',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.queue_url = settings.SQS_NEWS_QUEUE_URL

    def send_message(self, message):
        attempts = 0
        while attempts < 3:
            try:
                self.client.send_message(QueueUrl=self.queue_url, MessageBody=json.dumps(message, default=str))
                return
            except ClientError as exc:
                logger.error({'sqs_error': str(exc)})
                attempts += 1
        raise Exception('Failed to send message to SQS')
