from ..models.article import Article
from ..exceptions import ArticleNotFoundError


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
        try:
            article = Article.objects.get(article_number=article_number)
        except Article.DoesNotExist:
            raise ArticleNotFoundError(
                f"Article {article_number} does not exist yet."
            )
        
        article.publish()
        return article

    
