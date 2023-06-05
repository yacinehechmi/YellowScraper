from bs4 import BeautifulSoup as bs
from utils.Sql import Queries
from utils.dataclasses import Result, Results, Business, Access, \
                             Tripadvisor, Yellowpage, Foursquare
from settings import BASE_URL, DEFAULT_SETTINGS

from utils.logger import setup_logger

parse_logger = setup_logger('parse_logger', 'logs/parse.log')


class Parse:
    def __init__(self, results):
        self.results = results

    def updateCities(self, nearby_cities):
        if nearby_cities:
            for city_list in nearby_cities:
                for city in city_list.find_all('a', {'href': True}):
                    if city['href'] not in \
                                        [city for city in
                                         Results.getEndpointsNames()]:
                        Results.updateEndpoints(Result(city['href'], 0, 0, 1))

    def parsePagination(self, pagination):
        if pagination:
            pagination = pagination.text
            x = pagination[pagination.find('-')+1: pagination.rfind('o')-1]
            y = pagination[pagination.rfind(' ')+1: len(pagination)]
            return int(int(y)/int(x))
        else:
            return 0

    def updatePagination(self, page, soup):
        scraped = 0
        for res in Results.getEndpoints():
            if BASE_URL+res.endpoint == page.url:
                print(res.pages_scraped)
                scraped += 1
                res.total_pages = self.parsePagination(
                        soup.find('span', {'class': 'showing-count'})
                        )
                print(res.pages_scraped)
            res.updateScraped(scraped)

    def parseContentAndStore(self):
        for page in self.results:
            soup = bs(page, features='lxml')
            if not DEFAULT_SETTINGS:
                self.updateCities(soup.find('section',
                                  {'class': 'nearby-cities'}))
                self.updatePagination(page, soup)

            for item_index, item in enumerate(
                    soup.find_all('div', {"class": "info"})):
                yellowpage = Yellowpage(
                               item.find('div', {'class': 'ratings'})  # rating
                               )
                foursquare = Foursquare(
                        item.find('div',
                                  {'class': 'ratings'})  # foursquare_rating
                        )
                tripadvisor = Tripadvisor(
                        item.find('div', {'class': 'ratings'})  # tripadvisor
                        )
                access = Access(
                        item.find('div',
                                  {'class': 'open-status'}),  # open_status
                        item.find('a',
                                  {'class': 'track-visit-website',
                                   'href': True}),  # website
                        item.find('a',
                                  {'class': 'order-online',
                                      'href': True})  # order_online
                                  )
                business = Business(
                        item.find('a', {'class': 'business-name'}
                                  ),  # name
                        item.find('div',
                                  {'class': 'price-range'}
                                  ),  # price_range
                        item.find('div', {'class': 'number'}
                                  ),  # year_business
                        item.find('div',
                                  {'class': 'locality'}
                                  ),  # locality
                        item.find("div",
                                  {"class": "categories"}
                                  ),  # categories
                        item.find("div",
                                  {"class": "amenities-info"}
                                  )  # amenities
                        )
                record = [
                        (business.get_business(), business.query),
                        (access.get_access(), access.query),
                        (tripadvisor.get_tripadvisor(), tripadvisor.query),
                        (yellowpage.get_yellowpage(), yellowpage.query),
                        (foursquare.get_foursquare(), foursquare.query)
                        ]
                Queries().upsert(record)
