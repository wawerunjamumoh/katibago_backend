from django.contrib import admin
from ..models.learning_objectives import LearningObjective

class LearningObjectiveInline(admin.TabularInline):
    model = LearningObjective
    extra = 1

    fields = (
        "statement",
        "cognitive_level",
        "display_order",
    )

    show_change_link = True

