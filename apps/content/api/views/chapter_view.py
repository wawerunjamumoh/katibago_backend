from rest_framework import viewsets

from apps.content.models.chapter import Chapter
from ..serializers.chapter_serializer import ChapterSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    lookup_field="number"
