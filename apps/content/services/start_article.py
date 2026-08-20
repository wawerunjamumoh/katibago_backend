from django.utils import timezone

from ..models.article_progress import (
    ArticleProgress,
    ArticleProgressStatus,
)
from ..models.article import Article
from ..exceptions import ArticleNotReadyError


class StartArticleService:

    @staticmethod
    def execute(user, article_number):

        article = Article.objects.get(
            article_number=article_number
        )

        if not article.is_active:
            raise ArticleNotReadyError(
                "Article is not available."
            )

        now = timezone.now()

        progress, created = ArticleProgress.objects.get_or_create(
            user=user,
            article=article,
            defaults={
                "status": ArticleProgressStatus.IN_PROGRESS,
                "started_at": now,
                "last_accessed_at": now,
            },
        )

        if not created:
            progress.last_accessed_at = now
            progress.save(
                update_fields=["last_accessed_at"]
            )

        return progress


