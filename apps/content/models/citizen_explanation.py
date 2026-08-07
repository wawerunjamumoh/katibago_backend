from django.db import models
from .article import Article

class CitizenExplanation(models.Model):
    """
    Provides a plain-language explanation of a constitutional
    article for everyday citizens.

    This explanation is reusable across multiple Feedback records
    and complements the official constitutional text.
    """

    # ==========================
    # Relationships
    # ==========================

    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name="citizen_explanation",
        help_text="The article this explanation belongs to.",
    )

    # ==========================
    # Business Fields
    # ==========================

    explanation = models.TextField(
        help_text="Plain-language explanation of the constitutional principle"
    )

    # ==========================
    # System Fields
    # ==========================

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Citizen Explanation"
        verbose_name_plural = "Citizen Explanations"

    def __str__(self):
        return f"Citizen Explanation - Article {self.article.article_number}"