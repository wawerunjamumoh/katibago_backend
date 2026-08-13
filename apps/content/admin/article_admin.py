from django.contrib import admin, messages

# MODELS
from ..models.article import Article

# INLINES
from .learning_objective_inline import LearningObjectiveInline
from .citizen_explanation_inline import CitizenExplanationInline
from .official_constitution_inline import OfficialConstitutionInline
from .saftey_shield_inline import SafetyShieldInline

#SERVICES
from ..services.activate_article import ActivateArticleService
from ..services.deactivate_article import DeactivateArticleService
from ..services.publish_article import PublishArticleService

# ACTIONS
@admin.action(description="Publish selected articles")
def publish_articles(modeladmin, request, queryset):
    published = 0
    failed = 0

    for article in queryset:
        try:
            PublishArticleService.execute(article.id)
            published += 1
        except ValueError as exc:
            failed += 1
            modeladmin.message_user(
                request,
                f"Article {article.article_number}: {exc}",
                messages.ERROR,
            )

    if published:
        modeladmin.message_user(
            request,
            f"{published} article(s) published.",
            messages.SUCCESS,
        )

@admin.action(description="Activate selected Article")
def activate_articles(modeladmin,request,queryset):
    activated = 0
    failed = 0

    for article in queryset:
        try:
            ActivateArticleService.execute(article.id)
            activated += 1
        except ValueError as exc:
            failed += 1
            modeladmin.message_user(
                request,
                f"Article {article.article_number}: {exc}",
                messages.ERROR,
            )

    if activated:
        modeladmin.message_user(
            request,
            f"{activated} articles(s) activated",
            messages.SUCCESS,
        )

@admin.action(description="Deactivate selected article.")
def deactivate_article(modeladmin,request,queryset):
    deactivated = 0

    for article in queryset:
        DeactivateArticleService.execute(article.id)
        deactivated += 1

    modeladmin.message_user(
        request,
        f"{deactivated} article(s) deactivated.",
        messages.SUCCESS,
    )


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

    # Inlines
    inlines = [
        LearningObjectiveInline,
        CitizenExplanationInline,
        OfficialConstitutionInline,
        SafetyShieldInline,
    ]

    # Actions
    actions = [
        publish_articles,
    ]


