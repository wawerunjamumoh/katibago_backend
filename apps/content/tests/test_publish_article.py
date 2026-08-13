from django.test import TestCase

from apps.content.models.article import Article
from apps.content.services.publish_article import PublishArticleService


class PublishArticleServiceTestCase(TestCase):

    def test_service_publishes_ready_article(self):
        ...
