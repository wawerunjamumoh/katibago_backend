from rest_framework import serializers

from ...models.part import Part
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = (
            "id",
            "chapter",
            "title",
            "friendly_title",
            "display_order",
            "part_type",
        )

        read_only_fields=(
            "id",
        )
