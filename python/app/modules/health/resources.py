from ...utils import HttpUtils


class HealthResources(object):
    @staticmethod
    async def get(request):
        return HttpUtils.send_response({'message': 'I''m healthy! :)'})
