from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# CHAPTER MODEL
class Chapter(models.Model):
    """Model representing a chapter with official and citizen titles."""
    number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(18),
        ],
    )
    official_title = models.CharField(max_length=255, unique=True)
    citizen_title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Chapter model.

        Provides ordering and human-readable names for the model.
        """
        # Instructions about the model
        ordering = ["number"]  # give chapters in numerical order
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return f"Chapter {self.number}: {self.official_title}"

    def get_display_title(self):
        """Return the official title if present, otherwise the citizen title."""
        return self.official_title or self.citizen_title