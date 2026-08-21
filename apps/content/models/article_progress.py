from django.db import models
from .article import Article


class ArticleProgressStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"


class ArticleProgress(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE, 
        related_name="article_progress",
    )
    status = models.CharField(choices=ArticleProgressStatus.choices)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # one user cannot have multiple records for one lesson
        constraints = [
            models.UniqueConstraint(
                fields=["user", "article"],
                name="unique_article_progress_per_user",
            ),
        ]
