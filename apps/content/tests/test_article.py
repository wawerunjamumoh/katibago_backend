from django.test import TestCase

from apps.content.models.article import Article
from apps.content.models.part import Part
from apps.content.models.chapter import Chapter


class ArticleTestCase(TestCase):
    """Tests for article activation and publication behavior."""

    def setUp(self):
        self.chapter = Chapter.objects.create(  
            number=1,
            official_title="Foundations",
            citizen_title="The Foundations",
        )

        self.part = Part.objects.create( 
            chapter=self.chapter,
            title="General",
            friendly_title="Getting Started",
            display_order=1,
            
        )

        self.article = Article.objects.create(  
            part=self.part,
            article_number=1,
            official_title="The Right to Privacy",
            citizen_title="Your Right to Privacy",
            difficulty="easy",
            xp_reward=25,
            estimated_duration_seconds=60,
        )

    def test_unpublished_article_cannot_be_activated(self):
        self.assertFalse(self.article.is_published)
        self.assertFalse(self.article.is_active)

        with self.assertRaises(ValueError):
            self.article.activate()

        self.article.refresh_from_db()

        self.assertFalse(self.article.is_active)

    def test_published_article_can_be_activated(self):
        self.article.is_published = True
        self.article.save()

        self.article.activate()

        self.article.refresh_from_db()

        self.assertTrue(self.article.is_published)
        self.assertTrue(self.article.is_active)

    def test_active_article_can_be_deactivated(self):
        self.article.is_published = True
        self.article.is_active = True
        self.article.save()

        self.article.deactivate()

        self.article.refresh_from_db()

        self.assertFalse(self.article.is_active)
        self.assertTrue(self.article.is_published)

    def test_incomplete_article_cannot_be_published(self):
        with self.assertRaises(ValueError):
            self.article.publish()

        self.article.refresh_from_db()

        self.assertFalse(self.article.is_published)

    def test_ready_article_can_be_published(self):
        # Arrange
        # create 2 learning objectives
        # create citizen explanation
        # create official constitution
        # create safety shield
        # create case
        # connect case to article

        # Act
        self.article.publish()

        # Assert
        self.article.refresh_from_db()

        self.assertTrue(self.article.is_published)
