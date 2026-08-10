from django.contrib import admin
from ..models.official_constitution_text import OfficialConstitution

@admin.register(OfficialConstitution)
class OfficialConstitutionTextAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "constitution_text",
        "source_reference",

    )

    search_fields = (
        "article",
        "source_reference",
    )

    list_filter = (
        "article",
    )

    ordering = (
        "article__article_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "article",
    )

    list_select_related = (
        "article",
    )