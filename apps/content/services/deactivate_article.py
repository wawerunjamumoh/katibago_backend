from ..models.article import Article
from ..exceptions import ArticleNotFoundError   

class DeactivateArticleService:
    @staticmethod
    def execute(article_number: int) -> Article:
        try:
            article = Article.objects.get(article_number=article_number)
        except Article.DoesNotExist:
            raise ArticleNotFoundError(
                f"Article {article_number} does not exist yet."
            )

        article.deactivate()
        return article