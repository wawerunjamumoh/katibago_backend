from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.content.models.article import Article
from apps.content.models.article_progress import ArticleProgress, ArticleProgressStatus
from apps.content.models.case import Case
from apps.content.models.choice import Choice
from apps.content.models.decision_point import DecisionPoint
from apps.content.models.decision_response import DecisionResponse
from apps.content.models.learner_profile import LearnerProfile
from apps.content.models.part import Part
from apps.content.models.chapter import Chapter
from apps.content.services.complete_article import CompleteArticleService
from apps.content.services.start_article import StartArticleService


User = get_user_model()


class LearnerWorkflowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="learner",
            password="strong-password-123",
        )
        self.other_user = User.objects.create_user(
            username="other-learner",
            password="strong-password-123",
        )
        chapter = Chapter.objects.create(
            number=1,
            official_title="Foundations",
            citizen_title="The Foundations",
        )
        part = Part.objects.create(
            chapter=chapter,
            title="General",
            friendly_title="Getting Started",
            display_order=1,
        )
        self.article = Article.objects.create(
            part=part,
            article_number=19,
            official_title="Freedom and security",
            citizen_title="Your rights",
            estimated_duration_seconds=60,
            xp_reward=40,
            is_active=True,
        )
        case = Case.objects.create(
            case_title="A constitutional choice",
            summary="Choose an action.",
            story="A learner must decide what to do.",
        )
        self.decision_point = DecisionPoint.objects.create(
            case=case,
            prompt="What should the learner do?",
        )
        self.choice = Choice.objects.create(
            decision_point=self.decision_point,
            choice_text="Choose the lawful action.",
            display_order=1,
        )
        self.other_choice = Choice.objects.create(
            decision_point=self.decision_point,
            choice_text="Choose another action.",
            display_order=2,
        )
        other_decision = DecisionPoint.objects.create(
            case=case,
            prompt="A different decision.",
        )
        self.unrelated_choice = Choice.objects.create(
            decision_point=other_decision,
            choice_text="An unrelated choice.",
            display_order=1,
        )
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=self.user).key}"
        )

    def test_start_creates_user_owned_in_progress_record(self):
        progress = StartArticleService.execute(self.user, 19)

        self.assertEqual(progress.user, self.user)
        self.assertEqual(progress.status, ArticleProgressStatus.IN_PROGRESS)
        self.assertEqual(ArticleProgress.objects.filter(article=self.article).count(), 1)

    def test_complete_marks_progress_and_awards_xp(self):
        StartArticleService.execute(self.user, 19)

        progress, xp_awarded, total_xp = CompleteArticleService.execute(self.user, 19)

        self.assertEqual(progress.status, ArticleProgressStatus.COMPLETED)
        self.assertEqual(xp_awarded, 40)
        self.assertEqual(total_xp, 40)
        self.assertEqual(LearnerProfile.objects.get(user=self.user).xp, 40)

    def test_each_user_can_start_same_article(self):
        StartArticleService.execute(self.user, 19)
        other_progress = StartArticleService.execute(self.other_user, 19)

        self.assertEqual(other_progress.user, self.other_user)
        self.assertEqual(
            ArticleProgress.objects.filter(article=self.article).count(),
            2,
        )

    def test_my_progress_list_returns_only_authenticated_users_progress(self):
        StartArticleService.execute(self.user, 19)
        StartArticleService.execute(self.other_user, 19)

        response = self.client.get("/api/v1/me/progress/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["article"], self.article.id)

    def test_my_progress_detail_uses_article_number_and_is_user_scoped(self):
        StartArticleService.execute(self.other_user, 19)

        response = self.client.get("/api/v1/me/progress/19/")

        self.assertEqual(response.status_code, 404)

    def test_user_can_submit_and_update_decision_response(self):
        response = self.client.post(
            f"/api/v1/decisionpoints/{self.decision_point.id}/respond/",
            {"selected_choice": self.choice.id},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        saved_response = DecisionResponse.objects.get(user=self.user)
        self.assertEqual(saved_response.decision_point, self.decision_point)
        self.assertEqual(saved_response.selected_choice, self.choice)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["answered_at"], saved_response.answered_at.isoformat().replace("+00:00", "Z"))

        response = self.client.post(
            f"/api/v1/decisionpoints/{self.decision_point.id}/respond/",
            {"selected_choice": self.other_choice.id},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(DecisionResponse.objects.filter(user=self.user).count(), 1)
        saved_response.refresh_from_db()
        self.assertEqual(saved_response.selected_choice, self.other_choice)

    def test_decision_response_rejects_choice_from_another_decision(self):
        response = self.client.post(
            f"/api/v1/decisionpoints/{self.decision_point.id}/respond/",
            {"selected_choice": self.unrelated_choice.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(DecisionResponse.objects.count(), 0)
