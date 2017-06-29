from aiohttp import ClientSession
from pycld2 import detect
from re import compile

from .models import PageRaw


class ArticleExtractor(object):
    async def extract_article(self, content: str, url: str) -> dict:
        """Returns the article section of the given url."""

        raise NotImplementedError()


class ReadabilityArticleExtractor(ArticleExtractor):
    _READABILITY_URL = 'http://readability:5000/extract'

    def __init__(self, client_session: ClientSession):
        self._client_session = client_session

    async def extract_article(self, content: str, url: str) -> dict:
        async with self._client_session.post(
                ReadabilityArticleExtractor._READABILITY_URL,
                data={'url': url, 'content': content}) as response:
            assert response.status == 200, \
                'TextExtractor service returned status [%d].' % response.status
        json = await response.json()
        if not json:
            return {}
        return {'authors': json.get('byline'),
                'summary': json.get('excerpt'),
                'length': json.get('length'),
                'content_html': json.get('content'),
                'content_text': json.get('textContent'),
                'title': json.get('title')}


class PageFetcher(object):
    async def fetch_page(self, url: str) -> PageRaw:
        """Returns the full page of the given url."""

        raise NotImplementedError()


class HttpPageFetcher(PageFetcher):
    def __init__(self, client_session: ClientSession):
        self._client_session = client_session

    async def fetch_page(self, url: str) -> PageRaw:
        async with self._client_session.get(url) as response:
            assert response.status == 200, \
                'Unexpected status [%d].' % response.status
            content = await response.text()
            return PageRaw(content=content)


class DocumentExtractorService(object):
    _ARTICLE_LINK_REGEX = compile('href=\"([^\"]*)')
    _ARTICLE_IMAGE_REGEX = compile('src=\"([^\"]*)')

    def __init__(self, page_fetcher: PageFetcher,
                 article_extractor: ArticleExtractor):
        self._page_fetcher = page_fetcher
        self._article_extractor = article_extractor

    @staticmethod
    def _extract_page_info(article: dict, url: str) -> dict:
        """Extracts additional page information."""

        if not article:
            return {}
        language = detect(article.get('content_text'))
        if len(language) > 2 and len(language[2]) > 1:
            language_code = language[2][0][1]
        else:
            language_code = None
        return {'url': url, 'language': language_code}

    async def extract(self, url: str) -> dict:
        """Returns article content and page information for the given url.

        Returns:
            (dict): A dictionary with the values
                - article
                    - authors: The authors.
                    - summary: The article summary.
                    - length: The number of characters.
                    - title: The title.
                    - content_html: The article content in HTML with links.
                    - content_text: The article content in plain text.
                    - links: The external links.
                    - images: The images.
                - page
                    - url: The page url.
                    - language: The language code (2 digits).
                - insight (not yet implemented)
                    - entities: Entities name recognition.
        """

        page_raw = await self._page_fetcher.fetch_page(url)
        article = await self._extract_article_info(page_raw.content, url)
        page = self._extract_page_info(article, url)
        return {'article': article, 'page': page}

    async def _extract_article_info(self, content: str, url: str) -> dict:
        article = await self._article_extractor.extract_article(content, url)
        if not article:
            return {}
        article['links'] = list(set(self._ARTICLE_LINK_REGEX.findall(
            article.get('content_html'))))
        article['images'] = list(set(self._ARTICLE_IMAGE_REGEX.findall(
            article.get('content_html'))))
        return article
