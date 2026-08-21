from rest_framework import viewsets

from apps.content.models.part import Part
from ..serializers.part_serializer import PartSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class=PartSerializer
    lookup_field="display_order"