from ..serializers.article_progress_serializer import ArticleProgressSerializer
from apps.content.models.article_progress import ArticleProgress
from rest_framework import viewsets



class ArticleProgressViewSets(viewsets.ModelViewSet):
    queryset = ArticleProgress.objects.all()
    serializer_class = ArticleProgressSerializer
    lookup_field = "id"

    