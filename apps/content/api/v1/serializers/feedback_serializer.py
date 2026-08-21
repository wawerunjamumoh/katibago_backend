from rest_framework import serializers
from apps.content.models.feedback import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            "id",
            "choice",
            "citizen_explanation",
            "feedback_message",
            "performance_level",
        )
        read_only_fields = ("id",)
