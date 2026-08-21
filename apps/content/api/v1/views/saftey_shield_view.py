from rest_framework import viewsets
from apps.content.models.saftey_shield import SafteyShield
from ..serializers.saftey_shield_serializer import SafteyShieldSerializer

class SafteyShieldViewset(viewsets.ModelViewSet):
    queryset = SafteyShield.objects.all()
    serializer_class = SafteyShieldSerializer
    lookup_field =  "id"
