from django.conf import settings
from django.db import models


class LearnerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learner_profile",
    )
    xp = models.PositiveIntegerField(default=0)
    total_xp = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    streak_freeze_count = models.PositiveIntegerField(default=0)
    current_level = models.PositiveIntegerField(default=1)
    gems_balance = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.total_xp == 0 and self.xp:
            self.total_xp = self.xp
        if self.xp == 0 and self.total_xp:
            self.xp = self.total_xp
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Learner profile for {self.user.username}"
