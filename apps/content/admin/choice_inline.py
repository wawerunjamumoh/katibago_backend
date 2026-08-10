from django.contrib import admin
from ..models.choice import Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

    fields = (
        "choice_text",
        "display_order",
    )

    show_change_link = True