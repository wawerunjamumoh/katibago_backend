from ..models.article import Article

class ActivateArticleService:
    @staticmethod
    def execute(article_id: int) -> Article:
        article = Article.objects.get(pk=article_id)
        article.activate()
        return article