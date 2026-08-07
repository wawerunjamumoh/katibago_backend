from django.db import models
from .article  import Article
from .case import Case
from .usage_type import UsageType

class ArticleCase(models.Model):
    """Association between an article and a case with ordering metadata."""

    # Relationships
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_cases",
    )

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="article_cases",
    )

    # Business Fields
    display_order = models.PositiveSmallIntegerField()

    usage_type = models.CharField(
        max_length=20,
        choices=UsageType.choices,
        default=UsageType.INTRODUCTION,
    )

    is_required = models.BooleanField(default=True)

    # System
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["article", "display_order"]

        constraints = [

            models.UniqueConstraint(
                fields=["article", "case"],
                name="unique_case_per_article",
            ),

            models.UniqueConstraint(
                fields=["article", "display_order"],
                name="unique_case_order_per_article",
            ),
        ]

    def __str__(self):
        return f"{self.article} → {self.case}"
