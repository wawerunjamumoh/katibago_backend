from django.contrib import admin
from ..models.feedback import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "choice",
        "feedback_message",
        "performance_level"
    )

    search_fields = (
        "choice__choice_text",
        "feedback_message",
    )

    list_filter = (
        "feedback_message",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "choice",
    )