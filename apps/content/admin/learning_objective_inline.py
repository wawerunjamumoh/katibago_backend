from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from ..models.learning_objectives import LearningObjective

class LearningObjectiveInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        objectives = [
            form.cleaned_data
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        ]

        if len(objectives) < 2:
            raise forms.ValidationError("A case must have at least two learning objectives.")

class LearningObjectiveInline(admin.TabularInline):
    model = LearningObjective
    formset = LearningObjectiveInlineFormset

    extra = 1

    fields = (
        "statement",
        "cognitive_level",
        "display_order",
    )

    show_change_link = True

