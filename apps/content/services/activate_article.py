from ..models.article import Article

class ActivateArticleService:
    @staticmethod
    def execute(article_number: int) -> Article:
        article = Article.objects.get(
            article_number=article_number
        )
        article.activate()
        return article