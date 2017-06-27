from aiohttp import ClientSession
from pycld2 import detect
from re import compile

from .models import PageRaw


class ArticleExtractor(object):
    async def extract_article(self, content: str, url: str) -> dict:
        """Returns the article section of the given url."""

        raise NotImplementedError()


class ReadabilityArticleExtractor(ArticleExtractor):
    _READABILITY_URL = 'http://localhost:5000/extract'

    def __init__(self, client_session: ClientSession):
        self._client_session = client_session

    async def extract_article(self, content: str, url: str) -> dict:
        async with self._client_session.post(
                ReadabilityArticleExtractor._READABILITY_URL,
                data={'url': url, 'content': content}) as response:
            assert response.status == 200, \
                'TextExtractor service returned status [%d].' % response.status
        json = await response.json()
        return {'authors': json['byline'], 'summary': json['excerpt'],
                'length': json['length'], 'content_html': json['content'],
                'content_text': json['textContent'], 'title': json['title']}


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
    _PAGE_LINK_REGEX = compile('href=\"([^\"]*)')
    _ARTICLE_IMAGE_REGEX = compile('src=\"([^\"]*)')
    _SUFFIX_BLACKLIST = ['css', 'js']
    _PREFIX_BLACKLIST = ['javascript']

    def __init__(self, page_fetcher: PageFetcher,
                 article_extractor: ArticleExtractor):
        self._page_fetcher = page_fetcher
        self._article_extractor = article_extractor

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
                    - all_links: All the external links found in the page.
                - insight (not yet implemented)
                    - entities: Entities name recognition.
        """

        page_raw = await self._page_fetcher.fetch_page(url)
        article = await self._extract_article_info(page_raw.content, url)
        page = self._extract_page_info(page_raw, article, url)
        return {'article': article, 'page': page}

    async def _extract_article_info(self, content: str, url: str) -> dict:
        article = await self._article_extractor.extract_article(content, url)
        article['links'] = set(self._PAGE_LINK_REGEX.findall(
            article['content_html']))
        article['images'] = set(self._ARTICLE_IMAGE_REGEX.findall(
            article['content_html']))
        return article

    def _valid_link(self, link: str) -> bool:
        for prefix in self._PREFIX_BLACKLIST:
            if link.startswith(prefix):
                return False
        for suffix in self._SUFFIX_BLACKLIST:
            if link.endswith(suffix):
                return False
        return True

    def _extract_page_info(self, page_raw: PageRaw, article: dict, url: str) \
            -> dict:
        """Extracts additional page information."""

        language = detect(article['content_text'])
        if len(language) > 2 and len(language[2]) > 1:
            language_code = language[2][0][1]
        else:
            language_code = None
        all_links = set(self._PAGE_LINK_REGEX.findall(page_raw.content))
        all_links = [link for link in all_links if self._valid_link(link)]
        return {'url': url, 'language': language_code, 'all_links': all_links}
