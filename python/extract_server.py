#!/usr/bin/env python3.6
# Extractor server.

from aiohttp import web
from app.app import app


print('starting service at 127.0.0.1:8000')
web.run_app(app, host='127.0.0.1', port=8000)
