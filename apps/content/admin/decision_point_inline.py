from django.contrib import admin
from..models.decision_point import DecisionPoint

class DecisionPointInline(admin.TabularInline):
    model = DecisionPoint
    extra = 1
    fields = (
        "display_order",
    )
    show_change_link = True