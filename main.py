from bs4 import BeautifulSoup as bs
import logging
import asyncio
from utils.item import Business
from utils.helpers import find_nearby_cities
from utils.fetch import fetch
from sql.sql import do_upsert
from settings import settings


def parse_and_store(results, db, cities):
    # pretty sure there is a better way to do this
    run_once = False  # to run find_nearby_cities once in every url
    for page in results:
        soup = bs(page, features="lxml")  # added lxml to silence bs4 warning
        if not run_once:
            '''
            the find_nearby_cities() will parse nearby cities
            and pagination for each city and return them in a new dictionary
            '''
            new_cities = find_nearby_cities(soup.
                                            find('section',
                                                 {'class': 'nearby-cities'}),
                                            soup.
                                            find('div',
                                                 {'class': 'pagination'}),
                                            cities
                                            )
            if new_cities:
                run_once = True
        info_list = soup.find_all('div', {"class": "info"})
        for item_index, item in enumerate(info_list):
            '''
            call instance of class business and assign soup content
            to instance attributes
            the class will be responsible for cleaning the parsed data
            '''
            business = Business(
                    item_index,
                    item.find('a', {'class': 'business-name'}),  # name
                    item.find('div', {'class': 'phone'}),  # phone
                    item.find('div', {'class': 'locality'}),  # locality
                    item.find('div', {'class': 'price-range'}),  # price_range
                    item.find('div', {'class': 'open-status'}),  # open_status
                    item.find('div', {'class': 'result-rating'}),  # rating
                    item.find('div', {'class': 'count'}),  # rating_count
                    item.find('div', {'class': 'ratings'}),  # tripadvisor
                    item.find('div',
                              {'class': 'ratings'}),  # foursquare_rating
                    item.find_all("div",
                                  {"class": "categories"}),  # categories
                    item.find_all("div",
                                  {"class": "amenities-info"}),  # amenities
                    item.find('a',
                              {'class': 'track-visit-website',
                               'href': True}),  # website
                    item.find('a', {'class': 'order-online',
                                    'href': True}),  # order_online
                    item.find('div', {'class': 'number'}),  # year_in_business
                    )
            records = [
                business.get_business_info(),
                business.get_access_info(),
                business.get_yellowpages_info(),
                business.get_tripadvisor_info(),
                business.get_foursquare_info()
            ]
            do_upsert(db, records)
    return new_cities


def main(cities, db, pagination):
    results = None
    while True:
        if results:
            new_cities = parse_and_store(results, db, cities)
            if new_cities:
                results = asyncio.run(fetch(new_cities, pagination))
            else:
                break
        else:
            results = asyncio.run(fetch(cities, pagination))


if __name__ == "__main__":
    pagination = settings['pagination']
    cities = settings['cities']
    db = settings['db_creds']['db']
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='logs/scraper.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main(cities, db, pagination)
