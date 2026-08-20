from rest_framework import serializers

from apps.content.models.decision_point import DecisionPoint

class DecisionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionPoint
        fields = (
            "id",
            "case",
            "prompt",
            "display_order",
        )

        read_only_fields = (
            "id",
            "case",
        )