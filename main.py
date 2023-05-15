from bs4 import BeautifulSoup as bs
import logging
import asyncio
from utils.item import Business
from utils.scraper import build_cities_list
from utils.fetch import fetch
from sql.sql import do_upsert
from settings import settings


def parse_and_store(results, db):
    # get all elements with tag: div and class: info of a single page
    for page in results:
        soup = bs(page)
        card = soup.find_all('div', {"class": "info"})
        for i, j in enumerate(card):
            # call instance of class business and assign soup content to instance variables
            business = Business(
                    i,
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

cities = [
        '/beverly-hills-ca/retaurants',
        ]

db = settings['db_creds']['db']

def main(cities):
    results = None
    while True:
        if results:
            cities = build_cities_list(results, cities)
            results = asyncio.run(fetch(cities))
            parse_and_store(results, db)
        else: 
            results = asyncio.run(fetch(cities))
            parse_and_store(results, db)


if __name__ == "__main__":
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='logs/scraper.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main(cities)
