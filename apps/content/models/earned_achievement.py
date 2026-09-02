from django.conf import settings
from django.db import models

from .learner_profile import LearnerProfile


class EarnedAchievement(models.Model):
    learner_profile = models.ForeignKey(
        LearnerProfile,
        on_delete=models.CASCADE,
        related_name="achievements",
    )
    achievement_key = models.CharField(max_length=80)
    achievement_name = models.CharField(max_length=120)
    achievement_description = models.TextField(blank=True)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["learner_profile", "achievement_key"],
                name="unique_earned_achievement_per_profile",
            )
        ]
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.learner_profile.user.username} - {self.achievement_name}"
