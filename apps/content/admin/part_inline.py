from django.contrib import admin
from ..models.part import Part

class PartInline(admin.TabularInline):
    model = Part
    extra = 1
    fields = (
        "chapter",
        "title",
        "friendly_title",
        "display_order",
        "part_type"
    )
    show_change_link = True