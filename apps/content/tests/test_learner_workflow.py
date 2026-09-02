from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.content.models.article import Article
from apps.content.models.article_case import ArticleCase
from apps.content.models.article_progress import ArticleProgress, ArticleProgressStatus
from apps.content.models.case import Case
from apps.content.models.citizen_explanation import CitizenExplanation
from apps.content.models.choice import Choice
from apps.content.models.decision_point import DecisionPoint
from apps.content.models.decision_response import DecisionResponse
from apps.content.models.learning_objectives import LearningObjective
from apps.content.models.learner_profile import LearnerProfile
from apps.content.models.part import Part
from apps.content.models.chapter import Chapter
from apps.content.models.saftey_shield import SafteyShield
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
        ArticleCase.objects.create(
            article=self.article,
            case=case,
            display_order=1,
        )
        LearningObjective.objects.create(
            article=self.article,
            statement="Understand the right.",
            display_order=1,
        )
        CitizenExplanation.objects.create(
            article=self.article,
            explanation="A plain-language explanation.",
        )
        SafteyShield.objects.create(
            article=self.article,
            practical_guidance="Use the lawful process.",
            common_mistakes="Do not act recklessly.",
            when_to_seek_help="Seek help if the matter escalates.",
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

    def test_start_and_complete_http_actions_update_progress_and_award_xp(self):
        start_response = self.client.post("/api/v1/articles/19/start/")

        self.assertEqual(start_response.status_code, 200)
        self.assertEqual(start_response.data["status"], "in_progress")

        complete_response = self.client.post("/api/v1/articles/19/complete/")

        self.assertEqual(complete_response.status_code, 200)
        self.assertEqual(complete_response.data["status"], "completed")
        self.assertEqual(complete_response.data["xp_awarded"], 40)

        progress_response = self.client.get("/api/v1/me/progress/19/")
        self.assertEqual(progress_response.status_code, 200)
        self.assertEqual(progress_response.data["status"], "completed")

    def test_complete_marks_progress_and_awards_xp(self):
        StartArticleService.execute(self.user, 19)

        progress, xp_awarded, total_xp = CompleteArticleService.execute(self.user, 19)

        self.assertEqual(progress.status, ArticleProgressStatus.COMPLETED)
        self.assertEqual(xp_awarded, 40)
        self.assertEqual(total_xp, 40)
        self.assertEqual(LearnerProfile.objects.get(user=self.user).xp, 40)

    def test_me_profile_returns_summary_metrics(self):
        profile, _ = LearnerProfile.objects.get_or_create(user=self.user)
        profile.xp = 280
        profile.total_xp = 280
        profile.current_streak = 4
        profile.streak_freeze_count = 1
        profile.current_level = 3
        profile.gems_balance = 12
        profile.save()

        response = self.client.get("/api/v1/auth/me/profile/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_xp"], 280)
        self.assertEqual(response.data["current_streak"], 4)
        self.assertEqual(response.data["streak_freeze_count"], 1)
        self.assertEqual(response.data["current_level"], 3)
        self.assertEqual(response.data["gems_balance"], 12)
        self.assertEqual(response.data["badges"], [])
        self.assertEqual(response.data["achievements"], [])

    def test_each_user_can_start_same_article(self):
        StartArticleService.execute(self.user, 19)
        other_progress = StartArticleService.execute(self.other_user, 19)

        self.assertEqual(other_progress.user, self.other_user)
        self.assertEqual(
            ArticleProgress.objects.filter(article=self.article).count(),
            2,
        )

    def test_my_progress_list_returns_chapter_tree_with_article_progress(self):
        StartArticleService.execute(self.user, 19)
        StartArticleService.execute(self.other_user, 19)

        response = self.client.get("/api/v1/me/progress/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("chapters", response.data)
        self.assertEqual(response.data["chapters"][0]["number"], 1)
        self.assertEqual(
            response.data["chapters"][0]["official_title"],
            "Foundations",
        )
        self.assertEqual(
            response.data["chapters"][0]["parts"][0]["friendly_title"],
            "Getting Started",
        )
        self.assertEqual(
            response.data["chapters"][0]["parts"][0]["articles"][0]["article_number"],
            19,
        )
        self.assertEqual(
            response.data["chapters"][0]["parts"][0]["articles"][0]["status"],
            "unlocked",
        )
        self.assertEqual(
            response.data["chapters"][0]["parts"][0]["articles"][0]["progress"],
            0,
        )

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

    def test_learner_article_returns_aggregate_content_and_my_progress(self):
        StartArticleService.execute(self.user, 19)

        response = self.client.get("/api/v1/learn/articles/19/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["article"],
            {
                "article_number": 19,
                "title": "Your rights",
                "difficulty": "easy",
            },
        )
        self.assertEqual(response.data["learning_objectives"][0]["statement"], "Understand the right.")
        self.assertEqual(response.data["experiences"][0]["title"], "A constitutional choice")
        self.assertEqual(
            response.data["legal_explanation"],
            {"explanation": "A plain-language explanation."},
        )
        self.assertEqual(
            response.data["safety_shield"]["practical_guidance"],
            "Use the lawful process.",
        )
        self.assertEqual(response.data["progress"], {"status": "in_progress"})

    def test_learner_article_requires_authentication(self):
        response = APIClient().get("/api/v1/learn/articles/19/")

        self.assertEqual(response.status_code, 401)
