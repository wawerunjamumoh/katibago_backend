from ..models.article import Article

class PublishArticleService:
    """Service for publishing articles."""

    @staticmethod
    def execute(article_number) -> Article:
        """Publish an article and return it.
        Args:
            article_id: The article id to publish.
        Returns:
            The published article object.
        """
        article = Article.objects.get(article_number=article_number)
        article.publish()
        return article

    
