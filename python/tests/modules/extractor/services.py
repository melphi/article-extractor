from unittest import TestCase
from asyncio import get_event_loop

from app.modules.extractor.services import DocumentExtractorService
from tests.modules.extractor.mocks import MockArticleExtractor, MockPageFetcher
from tests.test_constants import TestConstants


class DocumentExtractorServiceTest(TestCase):
    def setUp(self):
        self._service = DocumentExtractorService(MockPageFetcher(),
                                                 MockArticleExtractor())
        self._event_loop = get_event_loop()

    def tearDown(self):
        self._event_loop.close()

    def test_extract_ru_mixed(self):
        data = self._event_loop.run_until_complete(self._service.extract(
            TestConstants.SAMPLE_DATA['RU_MIXED']['url']))

        article = data['article']
        self.assertIsNotNone(article)
        self.assertIsNone(article['authors'])
        self.assertIsNotNone(article['summary'])
        self.assertIsNotNone(article['length'])
        self.assertIsNotNone(article['title'])
        self.assertIsNotNone(article['content_html'])
        self.assertIsNotNone(article['content_text'])
        self.assertEqual(11, len(article['links']))
        self.assertEqual(3, len(article['images']))

        page = data['page']
        self.assertIsNotNone(page)
        self.assertIsNotNone(page['url'])
        self.assertEqual('ru', page['language'])
        self.assertEqual(118, len(page['all_links']))
