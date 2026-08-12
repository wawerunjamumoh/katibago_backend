from django.db import models
from .article import Article

class CognitiveLevel(models.TextChoices):
    """
    Expected level of learner thinking for this learning objective."""
    UNDERSTAND="Understand", "Understand"
    APPLY="Apply", "Apply"
    ANALYZE="Analyze", "Analyze"
    EVALUATE="Evaluate", "Evaluate"
    CREATE="Create", "Create"


class LearningObjective(models.Model):
    """"
    Represents a measurable learning outcome for an article.
    Learning objectives defines what learner should know or 
    be able to do after completing a lesson."""

    # def learning_objectives_ready(self):
    #     return self.learning_objectives.count() >= 2
    #===========================
    #Relationships
    #===========================
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="learning_objectives",
        help_text="The article this learning objective belongs to.",
    )

    #===========================
    #Business Fields
    #===========================
    statement = models.CharField(
        max_length=255,
        help_text="observable Learning outcome.",
    )

    #===========================
    #Educational Metadata
    #===========================
    cognitive_level = models.CharField(
        max_length=20,
        choices=CognitiveLevel.choices,
        default=CognitiveLevel.UNDERSTAND,
        help_text="Expected level of learner thinking for this learning objective.",
    )

    display_order = models.PositiveIntegerField(
        default=1,
        help_text="The order in which this learning objective should be displayed.",
    )

    #===========================
    #Audit
    #===========================
    created_at = models.DateTimeField(
        auto_now_add=True,)
    updated_at = models.DateTimeField(
        auto_now=True,)

    class Meta:
        ordering= ["article","display_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["article", "display_order"],
                name="unique_learning_objective_order_per_article",
            )
        ]

    def __str__(self):
        return f"{self.statement}"

