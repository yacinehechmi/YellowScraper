import requests
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# project mudules
from otherScripts.classBusiness import Business
from otherScripts.helpers import find_nearby_cities
from sql.sql import do_upsert
from Settings import settings


def scrape_clean_store(soup, db):
    # get all elements with tag: div and class: info of a single page
    card = soup.find_all('div', {"class": "info"})
    for i, j in enumerate(card):
        # call instance of class business and assign soup content to instance attributes
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


def fetch_page(num_of_page, city):
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
        return requests.get(f"https://www.yellowpages.com{city}", headers=headers, params={
                "page": num_of_page})
    except requests.HTTPError as errHTTP:
        logger.error(f" GOT {errHTTP} AT: num_of_page:{num_of_page} city:{city}")


def main():
    db = settings['db_creds']['db']
    cities = settings['cities']
    number_of_pages = settings['number_of_pages']
    csv_file_name = settings['csv_file_name']

    index = 0
    run_one_time = False
    while index < len(cities):
        for j in range(1, number_of_pages):
            # request yellowpages.com
            page = fetch_page(j, list(cities[index].keys())[0])
            page_content = page.content
            soup = BeautifulSoup(page_content, 'html.parser')
            # when find_nearby_cities finds new cities it will never run again unless the scraped city is changed
            if not run_one_time:
                # find nearby cities and append them to cities list if they don't exist
                if find_nearby_cities(soup.find('section', {"class": "nearby-cities"}), cities):
                    run_one_time = True
            scrape_clean_store(soup, db)
            # fetch_page HTTP GET request to www.yellowpage.com/{ city }/restaurants/?{ i }
        index += 1
    logger.info([city.values() for city in cities])


if __name__ == "__main__":
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='logs/scraper.log',
                        format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
