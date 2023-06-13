import asyncio
import httpx
from aiolimiter import AsyncLimiter
from fake_useragent import UserAgent
from utils.logger import setup_logger

fetch_logger = setup_logger("fetch_logger", "logs/fetch.log")


class Fetch():
    def __init__(self):
        self.tasks = []
        self.res = None
    # fetching per page

    async def fetch_page(self, client, url, limiter):
        async with limiter:
            try:
                # for random UserAgent for each request
                ua = UserAgent()
                user_agent = ua.random
                headers = {
                        "Accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"""
                        """image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Connection": "keep-alive",
                        "User-Agent": user_agent,
                        "Cache-Control": "max-age=0, no-cache, no-store",
                        "Upgrade-Insecure-Requests": "1"
                        }
                response = await client.get(url, headers=headers)
                return response
            except httpx.ReadError as e:
                fetch_logger.error(e)
            except httpx.ReadTimeout as e:
                fetch_logger.error(e)
            except httpx.ConnectTimeout as e:
                fetch_logger.error(e)
            except httpx.RequestError as e:
                fetch_logger.error(e)
            except httpx.NetworkError as e:
                fetch_logger.error(e)
            except (Exception, httpx.TimeoutException) as e:
                fetch_logger.error(e)

    async def fetch_all(self, session, requested):
        """
        loop through each page in each city and make an async request
        then gather those requests to be executed concurrently
        """
        limiter = AsyncLimiter(100, 0.1)
        async with httpx.AsyncClient() as client:
            for req in requested:
                for page in range(1, req.total_pages):
                    if page == 1:
                        url = f"https://www.yellowpages.com{req.endpoint}"
                    else:
                        url = f"""https://www.yellowpages.com{req.endpoint}?page={page}"""
                    self.tasks.append(self.fetch_page(
                        client,
                        url,
                        limiter
                        ))
            """
            added this while loop to make sure we get the requests
            pretty sure there is a better way to do this also
            """
            while not self.res:
                self.res = await asyncio.gather(*self.tasks)
            return self.res

    async def fetch(self, requested):
        async with httpx.AsyncClient() as session:
            return await self.fetch_all(session, requested)
