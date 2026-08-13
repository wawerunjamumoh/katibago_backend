from django.db import  models
from .article import Article

class SafteyShield(models.Model):
    """
    Provide practical guidance for applying an article's constitiutional principles in a real life situation.

    Saftey shield translates constitutional knowledge into safe,lawful and responsible actions.
    """

    # =============
    # Relationships
    # =============
    article = models.OneToOneField(
        Article ,
        on_delete = models.CASCADE,
        related_name = "saftey_shield",
        help_text="The article this article guide belongs to."
    )

    # ========================
    # Business Fields
    # ========================
    practical_guidance = models.TextField(
        help_text="Recommended lawful actions citizens should take."
    )

    common_mistakes=models.TextField(
        blank=True,
        help_text="Common misunderstandings of mistakes to avoid."
    )

    when_to_seek_help=models.TextField(
        blank=True,
        help_text="When to seek legal or professional help."
    )

    # ========================
    # System Fields
    # ========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Saftey Shield"
        verbose_name_plural = "Saftey Shields"

    def __str__(self):
        return f"Saftey Shield for {self.article.official_title}"
