from aiohttp import web


class HealthResources(object):
    @staticmethod
    async def get(request):
        return web.json_response({'message': 'I''m healthy! :)'})
