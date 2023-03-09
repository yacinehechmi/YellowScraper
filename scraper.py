import requests
import logging
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# project mudules
from classBusiness import Business
from helpers import find_nearby_cities
from sql import do_upsert
from process_to_csv import write_to_csv, clean_csv
from parameters import config

db = config['db']
cities = config['cities']
number_of_pages = config['number_of_pages']
csv_file_name = config['csv_file_name']


def scrape_clean_store(soup, db):
    # get all elements with tag: div and class: info
    # card = soup.find_all('div', _class="v-card")

    # print(soup.find_all('div', {"class": "info"}))
    card = soup.find_all('div', {"class": "info"})

    # loop through all info div's of a single page found by the soup
    for i, j in enumerate(card):
        # extantiate class business and assign soup content to class attributes
        business = Business(
            j.find('a', {'class': 'business-name'}),  # name
            j.find('div', {'class': 'phone'}),  # phone
            j.find('div', {'class': 'locality'}),  # locality
            j.find('div', {'class': 'price-range'}),  # price_range
            j.find('div', {'class': 'open-status'}),  # open_status
            j.find('div', {'class': 'result-rating'}),  # rating
            j.find('div', {'class': 'count'}),  # rating_count
            j.find('div', {'class': 'ratings'}),  # tripadvisor
            j.find('div', {'class': 'ratings'}),  # foursquare_rating
            j.find_all("div", {"class": "categories"}),  # categories
            j.find_all("div", {"class": "amenities-info"}),  # amenities
            j.find('a', {'class': 'track-visit-website', 'href': True}),  # website
            j.find('a', {'class': 'order-online', 'href': True}),  # order_online
            j.find('div', {'class': 'number'}),  # year_in_business
        )
        # values to be stored in business_info table
        business_info = (
                business.get_name(),
                business.get_phone(),
                business.get_price_range(),
                business.get_year_in_business(),
                business.get_amenities(),
                business.get_categories(),
                business.city,
                business.state_code,
                business.zip_code,
        )
        # values to be stored in access_info table
        access_info = (
            business.get_open_status(),
            business.get_website(),
            business.get_order(),
        )
        # values to be stored in yellowpages_info table
        yellowpages_info = (
            business.get_rating(),
            business.get_rating_count(),
        )
        # values to be stored in tripadvisor_info table
        tripadvisor_info = (
            business.get_tripadvisor_rating(),
            business.get_tripadvisor_rating_count(),
        )
        # values to be stored in foursquare_info table
        foursquare_info = (
            business.get_foursquare_rating(),
        )

        records = [
            business_info,
            access_info,
            yellowpages_info,
            tripadvisor_info,
            foursquare_info
        ]
        # connect to { db } & upsert { records } into tables business_info,
        # access_info, yellowpages_info, tripadvisor_info, foursquare_info

        do_upsert(db, records)
        # print(f'{i} time consumed : {time.time() - start}'


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
    run_one_time = False
    while index < len(cities):
        for j in range(1, number_of_pages):
            page = fetch_page(j, list(cities[index].keys())[0])
            page_content = page.content
            soup = BeautifulSoup(page_content, 'html.parser')
            if not run_one_time:
                if find_nearby_cities(soup.find('section', {"class": "nearby-cities"}), cities):
                    run_one_time = True
                # find nearby cities and append them to cities list

            scrape_clean_store(soup, db)
            # fetch_page HTTP GET request to www.yellowpage.com/{ city }/restaurants/?{ i }
        index += 1
    logger.info([city.values() for city in cities])

if __name__ == "__main__":
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='scraper.log',
                        format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
