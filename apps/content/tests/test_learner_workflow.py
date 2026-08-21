from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.content.models.article import Article
from apps.content.models.article_progress import ArticleProgress, ArticleProgressStatus
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
