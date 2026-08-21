from rest_framework import serializers

from apps.content.models.article import Article
from apps.content.models.article_case import ArticleCase
from apps.content.models.citizen_explanation import CitizenExplanation
from apps.content.models.learning_objectives import LearningObjective
from apps.content.models.saftey_shield import SafteyShield


class LearnerArticleSummarySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="citizen_title")

    class Meta:
        model = Article
        fields = ("article_number", "title", "difficulty")


class LearnerObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningObjective
        fields = ("statement", "cognitive_level", "display_order")


class LearnerExperienceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="case.case_title")
    summary = serializers.CharField(source="case.summary")
    story = serializers.CharField(source="case.story")

    class Meta:
        model = ArticleCase
        fields = (
            "id",
            "title",
            "summary",
            "story",
            "usage_type",
            "is_required",
            "display_order",
        )


class LearnerLegalExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenExplanation
        fields = ("explanation",)


class LearnerSafetyShieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafteyShield
        fields = (
            "practical_guidance",
            "common_mistakes",
            "when_to_seek_help",
        )


class LearnerProgressSerializer(serializers.Serializer):
    status = serializers.CharField(allow_null=True)


class LearnerArticleSerializer(serializers.Serializer):
    article = LearnerArticleSummarySerializer(source="*")
    learning_objectives = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    legal_explanation = serializers.SerializerMethodField()
    safety_shield = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    def get_learning_objectives(self, article):
        return LearnerObjectiveSerializer(
            article.learning_objectives.all(),
            many=True,
        ).data

    def get_experiences(self, article):
        return LearnerExperienceSerializer(
            article.case_assignment.select_related("case").all(),
            many=True,
        ).data

    def get_legal_explanation(self, article):
        explanation = getattr(article, "citizen_explanation", None)
        if explanation is None:
            return {}
        return LearnerLegalExplanationSerializer(explanation).data

    def get_safety_shield(self, article):
        safety_shield = getattr(article, "saftey_shield", None)
        if safety_shield is None:
            return {}
        return LearnerSafetyShieldSerializer(safety_shield).data

    def get_progress(self, article):
        user = self.context["request"].user
        progress = article.article_progress.filter(user=user).first()
        return LearnerProgressSerializer(
            {"status": progress.status if progress else None}
        ).data
