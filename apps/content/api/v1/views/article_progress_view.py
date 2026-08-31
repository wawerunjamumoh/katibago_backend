from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.content.models.article_progress import ArticleProgress
from ..serializers.article_progress_serializer import (
    ArticleProgressSerializer,
    MyProgressListSerializer,
)


class ArticleProgressViewSets(viewsets.ModelViewSet):
    queryset = ArticleProgress.objects.all()
    serializer_class = ArticleProgressSerializer
    lookup_field = "id"


class MyProgressListView(generics.GenericAPIView):
    serializer_class = MyProgressListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance={},
            context={"request": request},
        )
        return Response(serializer.data)

    def get_queryset(self):
        return ArticleProgress.objects.filter(
            user=self.request.user,
        ).select_related("article")


class MyProgressDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleProgressSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "article_number"

    def get_queryset(self):
        return ArticleProgress.objects.filter(
            user=self.request.user,
        ).select_related("article")

    def get_object(self):
        return generics.get_object_or_404(
            self.get_queryset(),
            article__article_number=self.kwargs[self.lookup_url_kwarg],
        )

    