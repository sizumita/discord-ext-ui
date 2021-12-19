from __future__ import annotations
from typing import Optional

import aiohttp
from aiohttp import ClientSession

from .async_publisher import AsyncPublisher


class URLRequestPublisher(AsyncPublisher):
    def __init__(self, url: str, session: Optional[ClientSession] = None):
        super().__init__()
        self.url = url
        self.session = session or ClientSession()

    async def dispatch(self) -> None:
        async with self.session:
            async with self.session.get(self.url) as resp:
                await self.upstream(resp)

    def json(self, *args, **kwargs) -> URLRequestPublisher:
        async def _json(resp: aiohttp.ClientResponse) -> dict:
            return await resp.json(*args, **kwargs)
        self.map(_json)
        return self
