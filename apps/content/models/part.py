from django.db import models
from .chapter import Chapter

class PartType(models.TextChoices):
    EXPLICIT = 'explicit',"Explicit constitutional Part"
    IMPLICIT = 'implicit',"Implicit Chapter Container"

class Part(models.Model):
    """
    Organises Articles within a chapter
    while distinguishing official constitutional parts
    from implicit container.
    """

    #Relationships
    chapter = models.ForeignKey(
        "Chapter",
        on_delete=models.CASCADE,
        related_name='parts'
    )

    #Business fields
    title = models.CharField(max_length=100)
    friendly_title = models.CharField(max_length=100,blank=True)
    display_order = models.PositiveSmallIntegerField()
    part_type = models.CharField(
        max_length=10,
        choices=PartType.choices
    )

    #System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["chapter","display_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter","display_order"],
                name="unique_part_order_per_chapter",
            )
        ]

    def __str__(self):
        return f"{self.title}"
