from rest_framework import viewsets
from apps.content.models.feedback import Feedback
from ..serializers.feedback_serializer import FeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class= FeedbackSerializer
    lookup_field = "id"
