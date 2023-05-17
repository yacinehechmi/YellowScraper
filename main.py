from bs4 import BeautifulSoup as bs
import logging
import asyncio
from utils.item import Business
from utils.scraper import build_cities_list
from utils.fetch import fetch
from sql.sql import do_upsert
from settings import settings


def parse_and_store(results, db):
    for page in results:
        soup = bs(page)
        info_list = soup.find_all('div', {"class": "info"})
        for item_index, item in enumerate(info_list):
            # call instance of class business and assign soup content to instance attributes
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
                    item.find('div', {'class': 'ratings'}),  # foursquare_rating
                    item.find_all("div", {"class": "categories"}),  # categories
                    item.find_all("div", {"class": "amenities-info"}),  # amenities
                    item.find('a', {'class': 'track-visit-website', 'href': True}),  # website
                    item.find('a', {'class': 'order-online', 'href': True}),  # order_online
                    item.find('div', {'class': 'number'}),  # year_in_business
                    )
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
            access_info = (
                    business.get_open_status(),
                    business.get_website(),
                    business.get_order(),
                    )
            yellowpages_info = (
                    business.get_rating(),
                    business.get_rating_count(),
                    )
            tripadvisor_info = (
                    business.get_tripadvisor_rating(),
                    business.get_tripadvisor_rating_count(),
                    )
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
            do_upsert(db, records)


def main(cities, db, pagination):
    results = None
    while True:
        if results:
            cities = build_cities_list(results, cities)
            if cities: 
                results = asyncio.run(fetch(cities, pagination))
                if results:
                    parse_and_store(results, db)
        else: 
            results = asyncio.run(fetch(cities, pagination))
            if results:
                parse_and_store(results, db)



if __name__ == "__main__":
    pagination = settings['pagination'] 
    cities = settings['cities']
    db = settings['db_creds']['db']
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='logs/scraper.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main(cities, db, pagination)
