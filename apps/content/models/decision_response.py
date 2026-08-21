from django.conf import settings
from django.db import models

from .choice import Choice
from .decision_point import DecisionPoint


class DecisionResponse(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decision_responses",
    )
    decision_point = models.ForeignKey(
        DecisionPoint,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.PROTECT,
        related_name="decision_responses",
    )
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "decision_point"],
                name="unique_decision_response_per_user",
            ),
        ]

    def __str__(self):
        return f"{self.user} response to decision {self.decision_point_id}"
