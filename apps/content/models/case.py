from django.conf import settings
from django.db import models

class Case(models.Model):
    """"
    A case is a real world classic scenario that aims at teaching how the law works in practice. It is a practical example of how the law is applied in real life situations.
    """

    # Relationships
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_cases",
        help_text="User who originally submitted the case.",
    )

    # Business Fields
    case_title = models.CharField(max_length=255)

    summary = models.CharField(max_length=255)

    story = models.TextField()

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Case model."""

        ordering = ["case_title"]
        verbose_name = "Case"
        verbose_name_plural = "Cases"

    def __str__(self):
        return f"{self.case_title}"

