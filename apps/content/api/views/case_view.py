from rest_framework import viewsets

from ...models.case import Case
from ..serializers.case_serializer import CaseSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    lookup_field = "id"
