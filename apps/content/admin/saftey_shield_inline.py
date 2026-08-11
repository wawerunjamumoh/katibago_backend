from django.contrib import admin
from ..models.saftey_shield import SafteyShield

class SafetyShieldInline(admin.StackedInline):
    model = SafteyShield
    extra = 0

    fields = (
        "practical_guidance",
        "common_mistakes",
        "when_to_seek_help",
    )

    show_change_link = True