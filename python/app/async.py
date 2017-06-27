from asyncio import Semaphore, get_event_loop
from aiohttp import ClientSession


# TODO: Implement https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
semaphore = Semaphore(1000)

client_session = ClientSession()
event_loop = get_event_loop()
