import aiohttp
import asyncio
from fake_useragent import UserAgent


async def fetch_page(session, url):
    async with session.get(url) as res:
        return await res.text()


async def fetch_all(session, cities):
    tasks = []
    # put the loops here, when looping through cities and num of pages
    print(type(cities))
    for city in cities:
        for page in range(30):
            if page > 1:
                url = f'https://www.yellowpages.com{city}/?page={page}'
            else:
                url = f'https://www.yellowpages.com{city}/'
            task = asyncio.create_task(fetch_page(session, url))
            tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def fetch(cities):
    ua = UserAgent()
    user_agent = ua.random
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "User-Agent": user_agent,
                "Cache-Control": "max-age=0, no-cache, no-store",
                "Upgrade-Insecure-Requests": "1"
                }
    async with aiohttp.ClientSession(headers = headers) as session:
        data = await fetch_all(session, cities)
        return data
