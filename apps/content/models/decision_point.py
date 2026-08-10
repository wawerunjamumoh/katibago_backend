from django.db import models


class DecisionPoint(models.Model):
    """
    Represents the single decision moment within a Case.

    A DecisionPoint groups the predefined Choices that a learner
    can select after reading the Case narrative.
    """

    case = models.OneToOneField(
        "Case",
        on_delete=models.CASCADE,
        related_name="decision_point",
        help_text="The case this decision belongs to.",
    )
    display_order = models.PositiveIntegerField(
        default=1,
        help_text="The order in which this decision point is displayed within the case.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Decision Point"
        verbose_name_plural = "Decision Points"

    def __str__(self):
        return f"Decision for {self.case.case_title}"
