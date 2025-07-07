from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import NewsWebhookSerializer
from .services import SQSService
from .authentication import TokenAuth
from apps.core.utils import logger


@method_decorator(csrf_exempt, name='dispatch')
class WebhookNewsView(APIView):
    authentication_classes = [TokenAuth]
    permission_classes = []

    def post(self, request):
        serializer = NewsWebhookSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                SQSService().send_message(data)
            except Exception as exc:
                logger.error({'error': str(exc)})
                return Response({'detail': 'error sending message'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'status': 'accepted'}, status=status.HTTP_201_CREATED)
        logger.warning({'invalid': serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
