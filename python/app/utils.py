from aiohttp.web import Response
from json import dumps


class HttpUtils(object):
    """Utility class to process aiohttp responses."""

    @staticmethod
    def send_response(data: dict=None, status: int=200) -> Response:
        text = dumps(data) if data else None
        return Response(text=text, status=status,
                        content_type='application/json')
