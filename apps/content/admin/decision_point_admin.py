from django.contrib import admin
from ..models.decision_point import DecisionPoint

@admin.register(DecisionPoint)
class DecisionPointAdmin(admin.ModelAdmin):
    list_display = (
        "case",
        "display_order",

    )

    search_fields = (
        "case",
    )

    list_filter = (
        "case",
    )

    ordering = (
        "case",
        "display_order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "case",
    )