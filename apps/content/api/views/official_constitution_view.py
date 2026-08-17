from rest_framework import viewsets
from ...models.official_constitution_text import OfficialConstitution
from ..serializers.official_constitution import OfficialConstitutionSerializer

class OfficialConstitutionViewSet(viewsets.ModelViewSet):
    queryset = OfficialConstitution.objects.all()
    serializer_class = OfficialConstitutionSerializer
    lookup_field = "id"
