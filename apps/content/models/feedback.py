from django.db import models
from .choice import Choice
from .citizen_explanation import CitizenExplanation

class PerformanceLevel(models.TextChoices):
    """"
    Performance levels for feedback.
    """

    EXCELLENT = "Excellent", "Excellent"
    GOOD = "Good", "Good"
    FAIR = "Fair", "Fair"
    NEEDS_IMPROVEMENT = "Needs Improvement", "Needs Improvement"


class Feedback(models.Model):
    """
    Provides educational coaching for a learner's selected Choice.

    Feedback explains the constitutional reasoning behind a Choice,
    evaluates the quality of the reasoning, and directs learners to
    a reusable CitizenExplanation for deeper understanding.
    """

    # ==========================
    # Relationships
    # ==========================

    choice = models.OneToOneField(
        Choice,
        on_delete=models.CASCADE,
        related_name="feedback",
        help_text="The choice this feedback explains.",
    )

    # citizen_explanation = models.ForeignKey(
    #     CitizenExplanation,
    #     on_delete=models.PROTECT,
    #     related_name="feedbacks",
    #     help_text="Reusable constitutional explanation supporting this feedback.",
    # )

    # ==========================
    # Business Fields
    # ==========================

    feedback_message = models.TextField(
        help_text="Coaching message explaining the learner's selected choice."
    )

    performance_level = models.CharField(
        max_length=25,
        choices=PerformanceLevel.choices,
        help_text="Educational evaluation of the learner's reasoning."
    )

    # ==========================
    # System Fields
    # ==========================

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["performance_level"]

        verbose_name = "Feedback"

        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"choice: {self.choice} /n Feedback: {self.feedback_message}"
