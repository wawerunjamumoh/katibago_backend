from django.contrib import admin
from ..models.choice import Choice
from django import forms

class ChoiceInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        choices = [
            form.cleaned_data
            for form in self.forms
            if form.cleaned_data
            and form.cleaned_data.get("choice_text")
            and not form.cleaned_data.get("DELETE", False)
        ]

        if len(choices) < 2:
            raise forms.ValidationError(
                "A decision point must have at least two choices."
            )

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    formset = ChoiceInlineFormSet

    fields = (
        "choice_text",
        "display_order",
    )

    show_change_link = True