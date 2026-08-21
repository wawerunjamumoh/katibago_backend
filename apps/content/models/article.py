from django.core.validators import MinValueValidator
from django.db import models
from ..exceptions import (
    ArticleNotReadyError,
    ArticleNotPublishedError,
    ArticleNotFoundError,
)

# from .chapter import Chapter
from .part import Part


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
    MIN_LEARNING_OBJECTIVES = 2

    # --------------------------------------------------
    # Domain behavior
    # --------------------------------------------------
    def is_ready_for_publication(self):
        """Return True if the article meets all readiness checks for publication.

        Combines learning objectives, legal content, and learning experience
        readiness checks.
        """
        return (
            self.learning_objectives_ready()
            and self.legal_content_ready()
            and self.learning_experience_ready()
        )

    def learning_objectives_ready(self):
        """Check if the article has the minimum required learning objectives."""
        return self.learning_objectives.count() >= self.MIN_LEARNING_OBJECTIVES

    def legal_content_ready(self):
        """Check if the article has all required legal content."""
        return all(
            [
                hasattr(self, "citizen_explanation"),
                hasattr(self, "official_constitution"),
                hasattr(self, "safety_shield"),
            ]
        )

    def learning_experience_ready(self):
        """Check if the article has at least one learning experience (case)."""
        # V1: Case is currently the only
        # implemented learning mechanism.
        return self.article_cases.exists()

    def publish(self):
        """Publish the article if it is ready."""
        if not self.is_ready_for_publication():
            raise ArticleNotReadyError(
                "Article is not ready for publication."
            )

        self.is_published = True
        self.save(update_fields=["is_published", "updated_at"])

    def activate(self):
        """Activate the article so learners can access it."""
        if not self.is_published:
            raise ArticleNotPublishedError(
                "Cannot activate an unpublished article."
            )

        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])

    def deactivate(self):
        """Deactivate the article so learners cannot access it."""
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    # ==========================================================
    # Relationships
    # ==========================================================

    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name="articles",
        help_text="The part this article belongs to.",
        null=True,
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

    is_published = models.BooleanField(
    default=False,
    help_text="Indicates whether this article has been published.",
    )

    is_active = models.BooleanField(
        default=False,
        help_text="Controls whether learners can currently access this lesson.",
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