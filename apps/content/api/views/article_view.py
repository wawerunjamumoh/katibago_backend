from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models.article import Article

from ...services.publish_article import PublishArticleService
from ...services.activate_article import ActivateArticleService
from ...services.deactivate_article import DeactivateArticleService


from ..serializers.article_serializer import ArticleSerializer

from ...exceptions import ArticleNotFoundError


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field="article_number"

    @action(detail=True,methods=["post"])
    def publish(self,request,article_number=None):
        article = PublishArticleService.execute(article_number)

        return Response(
            {
                "message": "Article published successfuly.",
                "article_number": article.article_number,
                "is_published": article.is_published,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def activate(self, request, article_number=None):
        article = ActivateArticleService.execute(article_number)

        return Response(
            {
                "message": "Article activated successfully.",
                "article_number": article.article_number,
                "is_active": article.is_active,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, article_number=None):
        article = DeactivateArticleService.execute(article_number)

        return Response(
            {
                "message": "Article deactivated successfully.",
                "article_number": article.article_number,
                "is_active": article.is_active,
            },
            status=status.HTTP_200_OK,
        )
