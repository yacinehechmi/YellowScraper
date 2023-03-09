import requests
import logging
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# project mudules
from classBusiness import Business
from helpers import find_nearby_cities
from sql import do_upsert, create_db_and_tables
from process_to_csv import write_to_csv, clean_csv
from parameters import config, upsert_into_tables


cities = config['cities']
number_of_pages = config['number_of_pages']
db = config['db']
csv_file_name = config['csv_file_name']


def fetch_page(num_of_page, city):
    try:
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
        return requests.get(f"https://www.yellowpages.com{city}", headers=headers, params={
                "page": num_of_page})
    except requests.HTTPError as errHTTP:
        logger.error(f" GOT {errHTTP} AT: num_of_page:{num_of_page} city:{city}")



def main():
    index = 0
    while index < len(cities):
        print(cities)
        for j in range(number_of_pages):
            page = fetch_page(j, list(cities[index].keys())[0])
            page_content = page.content
            soup = BeautifulSoup(page_content, 'html.parser')
            if j == 1:
                # find nearby cities and append them to cities list
                find_nearby_cities(soup.find('section', {"class": "nearby-cities"}), cities)
            scrape_clean_store(soup, db)
            # fetch_page HTTP GET request to www.yellowpage.com/{ city }/restaurants/?{ i }
        index += 1


if __name__ == "__main__":
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='scraper.log',
                        format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
