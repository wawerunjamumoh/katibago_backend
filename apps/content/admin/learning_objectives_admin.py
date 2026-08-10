from django.contrib import admin
from ..models.learning_objectives import LearningObjective    

@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "statement",
        "cognitive_level",
        "display_order",
    )

    search_fields = (
        "objective",
        "article__article_number",
        "statement",
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
    )

    list_select_related = (
        "article",
    )
