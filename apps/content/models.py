from django.db import models

class Chapter(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=255,unique=True)
    friendly_title = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Insructions about the model
        ordering = ["number"] #give chapters in numerical order
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        

    def __str__(self):
        return f"Chapter {self.number}: {self.title}"
