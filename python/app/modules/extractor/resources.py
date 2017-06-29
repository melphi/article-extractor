from aiohttp import web

from .components import extractor_service


class ExtractorResources(object):
    @staticmethod
    async def post(request):
        data = await request.json()
        if not data.get('url'):
            web.json_response({'error': 'Missing property url'}, status=400)
        result = await extractor_service.extract(data.get('url'))
        return web.json_response(result)
