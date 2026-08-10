from django.contrib import admin
from apps.content.models.usage_type import UsageType

@admin.register(UsageType)
class UsageTypeAdmin(admin.ModelAdmin):
    list_display = (
        "introduction",
        "primary",
        "supplementary",
    )