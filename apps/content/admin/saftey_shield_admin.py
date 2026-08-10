from django.contrib import admin
from ..models.saftey_shield import SafteyShield

@admin.register(SafteyShield)
class SafteyShieldAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "practical_guidance",
        "common_mistakes",
        "when_to_seek_help"
    )

    search_fields = (
        "practical_guidance",
    )

    list_filter = (
        "article",
        "practical_guidance",
    )

    ordering = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "article",
        "updated_at",
    )

    list_select_related = (
        "article",
    )