import aiohttp
import asyncio
from fake_useragent import UserAgent


async def fetch_page(session, url):
    try:
        ua = UserAgent()
        user_agent = ua.random
        headers = {
                'Accept': '''text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'''
                '''image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9''',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': user_agent,
                'Cache-Control': 'max-age=0, no-cache, no-store',
                'Upgrade-Insecure-Requests': '1'
                }
        async with session.get(url, headers=headers) as res:
            return await res.text()
    except aiohttp.ClientConnectorError as e:
        print('connection failed', str(e))
    except aiohttp.ClientOSError as e:
        print('connection failed', str(e))


async def fetch_all(session, cities, pagination):
    tasks = []
    # put the loops here, when looping through cities and num of pages
    for city, is_scraped in cities.items():
        if is_scraped:
            continue
        else:
            for page in range(1, pagination):
                if page == 1:
                    url = f'https://www.yellowpages.com{city}/'
                else:
                    url = f'https://www.yellowpages.com{city}/?page={page}'
                task = asyncio.create_task(fetch_page(session, url))
                tasks.append(task)
    res = None
    while not res:
        res = await asyncio.gather(*tasks)
    return res


async def fetch(cities, pagination):
    async with aiohttp.ClientSession() as session:
        return await fetch_all(session, cities, pagination)
