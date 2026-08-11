from django.contrib import admin
from ..models.article import Article
from .learning_objective_inline import LearningObjectiveInline
from .citizen_explanation_inline import CitizenExplanationInline
from .official_constitution_inline import OfficialConstitutionInline
from .saftey_shield_inline import SafetyShieldInline

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "article_number",
        "official_title",
        "citizen_title",
        "part",
        "difficulty",
        "is_active",
    )

    inlines = [
        LearningObjectiveInline,
        CitizenExplanationInline,
        OfficialConstitutionInline,
        SafetyShieldInline,
    ]

    search_fields = (
        "article_number",
        "official_title",
        "citizen_title",
    )

    list_filter = (
        "part",
        "difficulty",
        "is_active",
    )

    ordering = (
        "part",
        "article_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "part",
    )