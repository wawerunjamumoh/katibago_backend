from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.decision_point_serializer  import DecisionPointSerializer
from ..serializers.decision_response_serializer import DecisionResponseSerializer
from apps.content.models.decision_point import DecisionPoint
from apps.content.services.submit_decision_response import SubmitDecisionResponseService

class DecisionPointViewSet(viewsets.ModelViewSet):
    queryset = DecisionPoint.objects.all()
    serializer_class = DecisionPointSerializer
    lookup_field = "id"

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def respond(self, request, id=None):
        selected_choice = request.data.get("selected_choice")
        if selected_choice is None:
            raise serializers.ValidationError(
                {"selected_choice": "This field is required."}
            )

        try:
            selected_choice = int(selected_choice)
        except (TypeError, ValueError) as exc:
            raise serializers.ValidationError(
                {"selected_choice": "This field must be a choice ID."}
            ) from exc

        response = SubmitDecisionResponseService.execute(
            user=request.user,
            decision_point_id=self.get_object().id,
            selected_choice_id=selected_choice,
        )
        return Response(
            DecisionResponseSerializer(response).data,
            status=status.HTTP_201_CREATED,
        )
