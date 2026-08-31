from rest_framework import serializers

from apps.content.models.article_progress import ArticleProgress
from apps.content.models.chapter import Chapter
from apps.content.models.part import Part


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


class LearnerPartProgressSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source="display_order")
    friendly_title = serializers.CharField()
    articles = serializers.SerializerMethodField()

    class Meta:
        model = Part
        fields = ("number", "friendly_title", "articles")

    def get_articles(self, obj):
        request = self.context["request"]
        user_progress = {
            progress.article_id: progress
            for progress in ArticleProgress.objects.filter(
                user=request.user,
                article__part=obj,
            ).select_related("article")
        }

        highest_completed = max(
            (
                p.article.article_number
                for p in user_progress.values()
                if p.status == "completed"
            ),
            default=0,
        )

        article_list = []
        for article in obj.articles.all():
            progress = user_progress.get(article.id)
            if progress is not None and progress.status == "completed":
                status = "completed"
                progress_value = 100
            elif progress is not None and progress.status == "in_progress":
                status = "unlocked"
                progress_value = 0
            elif article.article_number <= highest_completed + 1:
                status = "unlocked"
                progress_value = 0
            else:
                status = "locked"
                progress_value = 0

            article_list.append(
                {
                    "article_number": article.article_number,
                    "citizen_title": article.citizen_title,
                    "status": status,
                    "progress": progress_value,
                }
            )
        return article_list


class LearnerChapterProgressSerializer(serializers.ModelSerializer):
    parts = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ("number", "official_title", "parts")

    def get_parts(self, obj):
        return LearnerPartProgressSerializer(
            obj.parts.all(),
            many=True,
            context={"request": self.context["request"]},
        ).data


class MyProgressListSerializer(serializers.Serializer):
    chapters = serializers.SerializerMethodField()

    def get_chapters(self, obj):
        chapters = Chapter.objects.filter(is_active=True).prefetch_related("parts__articles")
        return LearnerChapterProgressSerializer(
            chapters,
            many=True,
            context={"request": self.context["request"]},
        ).data