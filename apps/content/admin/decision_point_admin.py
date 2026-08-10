from django.contrib import admin
from ..models.decision_point import DecisionPoint
from .choice_inline import ChoiceInline

@admin.register(DecisionPoint)
class DecisionPointAdmin(admin.ModelAdmin):
    list_display = (
        "case",
        "display_order",
    )

    inlines = [
        ChoiceInline,
    ]

    search_fields = (
        "case",
    )

    list_filter = (
        "case",
    )

    ordering = (
        "case",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "case",
    )