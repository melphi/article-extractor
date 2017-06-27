from .components import extractor_service
from ...utils import HttpUtils


class ExtractorResources(object):
    @staticmethod
    async def post(request):
        data = await request.json()
        if not data.get('url'):
            HttpUtils.send_response({'error': 'Missing property url'}, 400)
        result = await extractor_service.extract()
        HttpUtils.send_response(result)
