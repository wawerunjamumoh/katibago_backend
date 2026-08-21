from rest_framework import serializers

from apps.content.models.chapter import Chapter


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = (
            "id",
            "number",
            "official_title",
            "citizen_title",
            "description",
            "parts"
        )

        read_only_fields = (
            "id",
            "parts",
        )
