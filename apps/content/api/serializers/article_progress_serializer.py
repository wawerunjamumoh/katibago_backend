from rest_framework import serializers


class ArticleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "article",
            "status",
            "started_at",
            "completed_at",
            "last_accessed_at",
        )

        read_only_fields = fields