from rest_framework import serializers
from ...models.choice import Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta():
        model = Choice
        fields = (
            "id",
            "decision_point",
            "choice_text",
            "display_order",
        )
        read_only_fields = (
            "id",
            "decision_point"
        )