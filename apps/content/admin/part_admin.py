from django.contrib import admin
from ..models.part   import Part
from .article_inline import ArticleInline


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = (
        "chapter",
        "title",
        "display_order",
        "part_type",
        "friendly_title",
    )

    inlines = [
        ArticleInline,
    ]

    search_fields = (
        "title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "title",
    )

    list_select_related = (
        "chapter",
    )
