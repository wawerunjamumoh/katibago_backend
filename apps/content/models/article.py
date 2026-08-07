from django.core.validators import MinValueValidator
from django.db import models

from .chapter import Chapter


class Difficulty(models.TextChoices):
    """
    Curriculum-defined difficulty level.
    """

    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"


class Article(models.Model):
    """
    Represents a learner-facing lesson based on a constitutional article.

    An Article belongs to a single Chapter and contains only the metadata
    required to deliver the lesson.

    Rich educational content (Cases, Learning Objectives,
    Citizen Explanations, Safety Shields, etc.) is linked through
    relationships and is intentionally not owned by this model.
    """

    # ==========================================================
    # Relationships
    # ==========================================================

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="articles",
        help_text="The constitutional chapter this article belongs to.",
    )

    # ==========================================================
    # Identity
    # ==========================================================

    article_number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
        ],
        help_text="Official article number in the Kenyan Constitution.",
    )

    # ==========================================================
    # Business Fields
    # ==========================================================

    official_title = models.CharField(
        max_length=255,
        help_text="Official constitutional title.",
    )

    citizen_title = models.CharField(
        max_length=255,
        help_text="Friendly learner-facing lesson title.",
    )

    # ==========================================================
    # Educational Metadata
    # ==========================================================

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
        help_text="Curriculum-defined lesson difficulty.",
    )

    xp_reward = models.PositiveSmallIntegerField(
        default=25,
        validators=[
            MinValueValidator(1),
        ],
        help_text="XP awarded after completing this lesson.",
    )

    estimated_duration_seconds = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(30),
        ],
        help_text="Estimated lesson duration in seconds.",
    )

    # ==========================================================
    # Publishing
    # ==========================================================

    is_active = models.BooleanField(
        default=False,
        help_text="Controls whether learners can access this lesson.",
    )

    # ==========================================================
    # Audit
    # ==========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["article_number"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f"Article {self.article_number}: {self.official_title}"