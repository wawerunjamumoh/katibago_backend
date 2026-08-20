from rest_framework import serializers
from apps.content.models.article_progress import ArticleProgress


class ArticleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleProgress
        fields = (
            "id",
            "article",
            "status",
            "started_at",
            "completed_at",
            "last_accessed_at",
        )

        read_only_fields = fields