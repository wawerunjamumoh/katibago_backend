from rest_framework import viewsets
from ..serializers.decision_point_serializer  import DecisionPointSerializer
from apps.content.models.decision_point import DecisionPoint

class DecisionPointViewSet(viewsets.ModelViewSet):
    queryset = DecisionPoint.objects.all()
    serializer_class = DecisionPointSerializer
    lookup_field = "id"
