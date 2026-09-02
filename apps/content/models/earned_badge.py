from django.conf import settings
from django.db import models

from .learner_profile import LearnerProfile


class EarnedBadge(models.Model):
    learner_profile = models.ForeignKey(
        LearnerProfile,
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge_key = models.CharField(max_length=80)
    badge_name = models.CharField(max_length=120)
    badge_description = models.TextField(blank=True)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["learner_profile", "badge_key"],
                name="unique_earned_badge_per_profile",
            )
        ]
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.learner_profile.user.username} - {self.badge_name}"
