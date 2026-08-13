from ..models.article import Article

class PublishArticleService:
    """Service for publishing articles."""

    @staticmethod
    def execute(article):
        """Publish an article and return it.
        Args:
            article: The article object or article id to publish.
        Returns:
            The published article object.
        """
        article = Article.objects.get(pk=article_id)
        article.publish()
        return article

    
