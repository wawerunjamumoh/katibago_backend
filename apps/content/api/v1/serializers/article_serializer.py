from rest_framework import serializers

from apps.content.models.article import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "article_number",
            "official_title",
            "citizen_title",
            "difficulty",
            "xp_reward",
            "estimated_duration_seconds",
            "is_published",
            "is_active",
            "article_progress",
        )
        read_only_fields = (
            "id",
            "is_published",
            "is_active",
        )
