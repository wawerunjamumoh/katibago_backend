from django.test import TestCase

from apps.content.models.article import Article
from apps.content.services.publish_article import PublishArticleService


class PublishArticleServiceTestCase(TestCase):

    def test_service_publishes_ready_article(self):
        from unittest.mock import patch, MagicMock
        with patch('apps.content.services.publish_article.Article.objects.get') as mock_get:
            mock_article = MagicMock()
            mock_get.return_value = mock_article

            result = PublishArticleService.execute(45)

            mock_get.assert_called_once_with(pk=45)
            mock_article.publish.assert_called_once()
            self.assertEqual(result, mock_article)
