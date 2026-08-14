from ..models.article import Article

class DeactivateArticleService:
    @staticmethod
    def execute(article_number: int) -> Article:
        article = Article.objects.get(
            article_number=article_number
        )
        article.deactivate()
        return article