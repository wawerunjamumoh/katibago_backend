from django.contrib import admin

from .models import Chapter

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "official_title",
        "citizen_title",
        "is_active"
    )
    ordering = ("number",)
    list_editable = ("is_active",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
