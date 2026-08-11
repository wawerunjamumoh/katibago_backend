from django.contrib import admin
from ..models.citizen_explanation import CitizenExplanation

class CitizenExplanationInline(admin.StackedInline):
    model = CitizenExplanation
    extra = 0

    fields = (
        "explanation",
    )

    show_change_link = True