from django.db import models

from apps.content.models.decision_point import DecisionPoint

class Choice(models.Model):
    """Represents a selectable choice for a decision point."""

    decision_point = models.ForeignKey(
        DecisionPoint,
        on_delete=models.CASCADE,
        related_name="choices",
    )

    

    choice_text = models.TextField()

    display_order = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["decision_point", "display_order"]

        constraints = [
            models.UniqueConstraint(
                fields=["decision_point", "display_order"],
                name="unique_choice_order_per_decision",
            )
        ]