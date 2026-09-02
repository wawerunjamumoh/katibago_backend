from django.conf import settings
from django.db import models


class LearnerEventLog(models.Model):
    EVENT_TYPES = (
        ("ARTICLE_COMPLETED", "Article Completed"),
        ("APP_OPENED", "App Opened"),
        ("BADGE_EARNED", "Badge Earned"),
        ("ACHIEVEMENT_EARNED", "Achievement Earned"),
        ("STREAK_FROZEN", "Streak Frozen"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learner_event_logs",
    )
    event_type = models.CharField(max_length=40, choices=EVENT_TYPES)
    event_payload = models.JSONField(default=dict, blank=True)
    timezone_offset_minutes = models.IntegerField(default=0)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [models.Index(fields=["user", "event_type", "occurred_at"]) ]

    def __str__(self):
        return f"{self.user_id}: {self.event_type}"
