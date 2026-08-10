from django.contrib import admin
from ..models.citizen_explanation import CitizenExplanation

@admin.register(CitizenExplanation)
class CitizenExplanationAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "explanation",
    
    )

    search_fields = (
        "article__article_number",
        "explanation",
    )


    ordering = (
        "article__article_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "article",
    )
