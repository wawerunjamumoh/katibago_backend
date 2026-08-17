from rest_framework import viewsets
from ...models.learning_objectives import LearningObjective
from ..serializers.learning_objectives import LearningObjectivesSerializer

class LearnimgObjectivesViewSet(viewsets.ModelViewSet):
    queryset = LearningObjective.objects.all()
    serializer_class = LearningObjectivesSerializer
    lookup_field = "id"