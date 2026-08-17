from rest_framework import serializers

from ...models.case import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields=(
            "id",
            "case_title",
            "summary",
            "story",
            "created_by"
        )

        read_only_fields = (
            "id",
        )