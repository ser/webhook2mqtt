#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import aiohttp_debugtoolbar
import asyncio
import glob
import logging
import random
import yaml
from aiohttp import web
from aiohttp_debugtoolbar import toolbar_middleware_factory
from cache import AsyncTTL
from prometheus_async import aio

logging.basicConfig(format='%(message)s',
                    level=logging.INFO)
log = logging.getLogger("w2m")

#@AsyncTTL(time_to_live=60)

# WEB SERVER LOOP
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    log.info(f'headers: {request.headers}')
    log.info(f'query: {request.query}')
    log.info(f'body: {await request.read()}')
    log.info(f'post: {await request.post()}')
    return web.Response(text="YAY!")

async def main():
    app = web.Application()
    aiohttp_debugtoolbar.setup(app)
    app.router.add_get("/metrics", aio.web.server_stats)
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 9245)
    await site.start()
    log.info("======= Serving ======")
    while True:
        await asyncio.sleep(100*3600)

loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    pass
loop.close()

# the end.
