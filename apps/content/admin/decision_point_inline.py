from django.contrib import admin
from..models.decision_point import DecisionPoint
from django import forms

class DecisionPointInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        decision_points = [
            form.cleaned_data
            for form in self.forms
            if form.cleaned_data
            and not form.cleaned_data.get("DELETE", False)
        ]

        if len(decision_points) < 1:
            raise forms.ValidationError(
                "A case must have at least one decision point."
            )

class DecisionPointInline(admin.TabularInline):
    model = DecisionPoint
    extra = 1
    formset = DecisionPointInlineFormSet
    fields = (
        "prompt",
        "display_order",
    )
    show_change_link = True
