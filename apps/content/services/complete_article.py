from django.db import transaction
from django.utils import timezone

from ..models.article_progress import ArticleProgress, ArticleProgressStatus
from ..models.learner_profile import LearnerProfile

from ..exceptions import ArticleNotStartedError


class CompleteArticleService:

    @staticmethod
    @transaction.atomic
    def execute(user, article_number):

        progress = ArticleProgress.objects.get(
            user=user,
            article__article_number=article_number,
        )

        if progress.status != ArticleProgressStatus.IN_PROGRESS:
            raise ArticleNotStartedError(
                "Article must be in progress before it can be completed."
            )

        progress.status = ArticleProgressStatus.COMPLETED
        progress.completed_at = timezone.now()

        progress.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )

        profile, _ = LearnerProfile.objects.get_or_create(user=user)
        profile.xp += progress.article.xp_reward
        profile.save(update_fields=["xp"])

        return progress, progress.article.xp_reward, profile.xp
