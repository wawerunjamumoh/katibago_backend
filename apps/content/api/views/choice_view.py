from rest_framework import viewsets
from ...models.choice import Choice
from ..serializers.choice_serializer import ChoiceSerializer

class ChoiceViewset(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class=ChoiceSerializer
    lookup_field = "id"
