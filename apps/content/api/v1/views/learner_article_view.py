from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.models.article import Article

from ..serializers.learner_article_serializer import LearnerArticleSerializer


class LearnerArticleDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LearnerArticleSerializer

    def get_object(self):
        return get_object_or_404(
            Article.objects.prefetch_related(
                "learning_objectives",
                "case_assignment__case",
            ),
            article_number=self.kwargs["article_number"],
            is_active=True,
        )
