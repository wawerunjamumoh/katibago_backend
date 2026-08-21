from django.utils import timezone

from ..models.choice import Choice
from ..models.decision_point import DecisionPoint
from ..models.decision_response import DecisionResponse


class SubmitDecisionResponseService:
    @staticmethod
    def execute(user, decision_point_id, selected_choice_id):
        try:
            decision_point = DecisionPoint.objects.get(pk=decision_point_id)
            choice = Choice.objects.get(
                pk=selected_choice_id,
                decision_point=decision_point,
            )
        except (DecisionPoint.DoesNotExist, Choice.DoesNotExist) as exc:
            raise ValueError("The selected choice is not valid for this decision.") from exc

        response, _ = DecisionResponse.objects.update_or_create(
            user=user,
            decision_point=decision_point,
            defaults={
                "selected_choice": choice,
                "answered_at": timezone.now(),
            },
        )
        return response