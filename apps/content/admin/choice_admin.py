from django.contrib import admin
from ..models.choice import Choice

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "decision_point",
        "choice_text",
        "display_order",
    )

    search_fields = (
        "decision_point__case__title",
        "choice_text",
    )


    ordering = (
        "decision_point__case__case_title",
        "decision_point__display_order",
        "display_order",
    )

    readonly_fields = (
        # "decision_point",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "decision_point",
        "decision_point__case",
    )