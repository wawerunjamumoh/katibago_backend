from rest_framework import viewsets

from apps.content.models.case import Case
from ..serializers.case_serializer import CaseSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    lookup_field = "id"
