import aiohttp
from dataclasses import dataclass


@dataclass
class News:
    url: str = None

    async def get_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                return await resp.text()
