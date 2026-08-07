from django.db import models
from .article import Article

class OfficialConstitution(models.Model):
    """
    Stores official constitutional text associated with the article.

    This model preserves the authentic wording of the constitution and serves as the authoritative legal reference of katibaGo.
    """

    #=============
    # Relationships
    #=============
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name="official_constitution",
        help_text="Official wording of the article from the constitution."
    )

    #=============
    # Business Fields
    #=============
    constitution_text = models.TextField(
        help_text="Official wording of the article from the constitution."
    ) 

    source_reference = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reference to the source of the official constitutional text or edition."
    )

    #=============
    # System fields
    #=============
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Article {self.article.article_number} Constitution"