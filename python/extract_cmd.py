#!/usr/bin/env python3.6
# Standalone command to extract a single page.

import asyncio
from argparse import ArgumentParser
from app.modules.extractor.services import DocumentExtractorService


def _extract(args: any) -> dict:
    loop = asyncio.get_event_loop()
    with DocumentExtractorService(loop) as extractor:
        data = loop.run_until_complete(extractor.extract(args.url))
    loop.close()
    return data

if __name__ == '__main__':
    parser = ArgumentParser(description='Extract web document.')
    parser.add_argument('url', type=str, help='The url to be processed.')
    result = _extract(parser.parse_args())
    print(result)
