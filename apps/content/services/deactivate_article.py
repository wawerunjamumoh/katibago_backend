from ..models.article import Article

class DeactivateArticleService:
    @staticmethod
    def execute(article_id: int) -> Article:
        article = Article.objects.get(pk=article_id)
        article.deactivate()
        return article