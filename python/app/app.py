from aiohttp import web

from .async import event_loop
from .modules.health.resources import HealthResources
from .modules.extractor.resources import ExtractorResources


app = web.Application(loop=event_loop)
app.router.add_get('/health', HealthResources.get)
app.router.add_post('/extract', ExtractorResources.post)
