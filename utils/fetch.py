from fake_useragent import UserAgent

import requests
import logging

logger = logging.getLogger(__name__)


def fetch_page(num_of_page, city):
    print(num_of_page, city)
    try:
        # randomize header's user_agent
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
        print('got it')
        return requests.get(f"https://www.yellowpages.com{city}", headers=headers, params={
                "page": num_of_page})
    except requests.HTTPError as errHTTP:
        logger.error(f" GOT {errHTTP} AT: num_of_page:{num_of_page} city:{city}")
