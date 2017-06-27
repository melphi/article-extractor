from app.modules.extractor.services import ArticleExtractor, PageFetcher
from app.modules.extractor.models import PageRaw
from tests.test_constants import TestConstants
from tests.test_utils import FileUtils


class MockArticleExtractor(ArticleExtractor):
    async def extract_article(self, content: str, url: str) -> dict:
        for key, value in TestConstants.SAMPLE_DATA.items():
            if url == value['url']:
                assert content == FileUtils.read_text(value['page']), \
                    'Unexpected content.'
            return FileUtils.read_json(value['article'])
        raise Exception('Page not found for [%s]' % url)


class MockPageFetcher(PageFetcher):
    async def fetch_page(self, url: str) -> PageRaw:
        for key, value in TestConstants.SAMPLE_DATA.items():
            if url == value['url']:
                return PageRaw(content=FileUtils.read_text(value['page']))
        raise Exception('Page not found for [%s]' % url)
