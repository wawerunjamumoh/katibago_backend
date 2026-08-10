from django.contrib import admin
from ..models.article import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "article_number",
        "official_title",
        "citizen_title",
        "chapter",
        "difficulty",
        "is_active",
    )

    search_fields = (
        "article_number",
        "official_title",
        "citizen_title",
    )

    list_filter = (
        "chapter",
        "difficulty",
        "is_active",
    )

    ordering = (
        "chapter",
        "article_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "chapter",
    )