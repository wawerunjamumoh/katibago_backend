from rest_framework import serializers

from apps.content.models.decision_response import DecisionResponse


class DecisionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionResponse
        fields = (
            "id",
            "user",
            "decision_point",
            "selected_choice",
            "answered_at",
        )
        read_only_fields = (
            "id",
            "user",
            "decision_point",
            "answered_at",
        )