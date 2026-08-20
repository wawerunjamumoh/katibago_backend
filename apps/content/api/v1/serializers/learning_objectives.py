from rest_framework import serializers

from apps.content.models.learning_objectives import LearningObjective

class LearningObjectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model= LearningObjective
        fields = (
            "id",
            "article",
            "statement",
            "cognitive_level",
            "display_order",
        )
        read_only_fields = (
            "id",
            "article"
        )
