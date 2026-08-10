from django.contrib import admin
from ..models.official_constitution_text import OfficialConstitution

class OfficialConstitutionInline(admin.StackedInline):
    model = OfficialConstitution
    extra = 0

    fields = (
        "constitution_text",
        "source_reference",
    )

    show_change_link = True