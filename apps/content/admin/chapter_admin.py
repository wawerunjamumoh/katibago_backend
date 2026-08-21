from django.contrib import admin
# from .article_inline import ArticleInline
from ..models import Chapter
# from ..models.part import Part
from .part_inline import PartInline

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    def part_count(self,obj):
        return obj.parts.count()

    list_display = (
        "number",
        "official_title",
        "citizen_title",
        "part_count",
        "is_active"
    )

    inlines = [
        PartInline,
    ]

    ordering = ("number",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "number",
        "official_title",
        "citizen_title",
    )

    list_filter = (
        "is_active",
    )
