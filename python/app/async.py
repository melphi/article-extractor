import asyncio
from aiohttp import ClientSession
from uvloop import new_event_loop


# TODO: Consider Semaphores
# https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

event_loop = new_event_loop()
asyncio.set_event_loop(event_loop)
client_session = ClientSession(loop=event_loop)
