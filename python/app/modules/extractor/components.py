from .services import (HttpPageFetcher, ReadabilityArticleExtractor,
                       DocumentExtractorService)
from ...async import client_session


_page_fetcher = HttpPageFetcher(client_session)
_article_extractor = ReadabilityArticleExtractor(client_session)
extractor_service = DocumentExtractorService(_page_fetcher, _article_extractor)
