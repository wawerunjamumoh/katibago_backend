from django.contrib import admin
from apps.content.models.case import Case
from .decision_point_inline import DecisionPointInline

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        "case_title",
        "summary",
        "created_by",
    )

    inlines = [
        DecisionPointInline,  
    ]

    search_fields = (
        "case_title",
        "summary",
        "story",
    )

    list_filter = (
        "created_by",
        "case_title",
    )

    ordering = (
        "case_title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "created_by",
    )

