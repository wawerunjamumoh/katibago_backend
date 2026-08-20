from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.content.models.article import Article

from apps.content.services.publish_article import PublishArticleService
from apps.content.services.activate_article import ActivateArticleService
from apps.content.services.deactivate_article import DeactivateArticleService
from apps.content.services.start_article import StartArticleService
from apps.content.services.complete_article import CompleteArticleService


from ..serializers.article_serializer import ArticleSerializer



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field="article_number"

    @action(detail=True,methods=["post"], permission_classes=[IsAuthenticated])
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

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
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

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
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

    @action(detail=True, methods=["post"],permission_classes=[IsAuthenticated],)
    def start(self, request, article_number=None):

        progress = StartArticleService.execute(
            article_number=article_number,
            user=request.user,
        )

        return Response(
            {
                "message": "Article started successfully.",
                "article_number": progress.article.article_number,
                "status": progress.status,
                "started_at": progress.started_at,
            }
        )

    @action(detail=True, methods=["post"],permission_classes=[IsAuthenticated],)
    def complete(self, request, article_number=None):

        progress = CompleteArticleService.execute(
            article_number=article_number,
            user=request.user,
        )

        return Response(
            {
                "message": "Article completed successfully.",
                "article_number": progress.article.article_number,
                "status": progress.status,
                "completed_at": progress.completed_at,
            }
        )
