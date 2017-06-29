#!/usr/bin/env python3.6
# Extractor server.

from aiohttp import web
from app.app import app


web.run_app(app, host='0.0.0.0', port=8000)
