#!/usr/bin/env python3.6
# Extractor server.

from aiohttp import web
from app.app import app


web.run_app(app, port=8000)
