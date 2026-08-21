from rest_framework import serializers
from apps.content.models.saftey_shield import SafteyShield

class SafteyShieldSerializer(serializers.ModelSerializer):
    class Meta():
        model = SafteyShield
        fields = (
            "id",
            "article",
            "practical_guidance",
            "common_mistakes",
            "when_to_seek_help"
        )

        read_only_fields = ("id",)
