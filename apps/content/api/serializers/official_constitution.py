from rest_framework import serializers
from ...models.official_constitution_text import OfficialConstitution

class OfficialConstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialConstitution
        fields = (
            "id",
            "article",
            "constitution_text",
            "source_reference",
        )
        read_only_fields = ("id",)
