import aiohttp
import asyncio
from fake_useragent import UserAgent


# fetching per page
async def fetch_page(session, url):
    try:
        # for random UserAgent for each request
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
    '''
    loop through each page in each city and make an async request
    then gather those request to be executed concurrently
    '''
    tasks = []
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
    '''
    added this while loop to make sure we get the requests
    pretty sure there is a better way to do this also
    '''
    while not res:
        res = await asyncio.gather(*tasks)
    return res


async def fetch(cities, pagination):
    # getting the new cities dict to be fetched
    async with aiohttp.ClientSession() as session:
        return await fetch_all(session, cities, pagination)
