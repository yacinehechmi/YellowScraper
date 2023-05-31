from bs4 import BeautifulSoup as bs
from utils.dataclasses import Result, Results, Business, Access, \
                             Tripadvisor, Yellowpage, Foursquare
from settings import settings


class Parse:
    def __init__(self, results):
        self.results = results

    def parseNearbyCities(self, nearby_cities):
        if nearby_cities:
            for city_list in nearby_cities:
                for city in city_list.find_all('a', {'href': True}):
                    if city['href'] not in \
                                        [city for city in
                                         Results.getEndpointsNames()]:
                        Results.updateEndpoints(Result(city['href'], 0, 0, 3))

    def parsePagination(self, pagination):
        if pagination is not None:
            pag_str = pagination.find('span')
            pag_str = str(pag_str)
            if pag_str:
                x = pag_str[pag_str.find('-')+1: pag_str.rfind('o')-1]
                y = pag_str[pag_str.rfind(' ')+1: len(pag_str)]
                if len(x) & len(y):
                    return int(int(pag_str[y])/int(pag_str[x]))
                else:
                    return 0

    def parseContentAndStore(self):
        for page in self.results:
            if page:
                print(page.url)
                soup = bs(page)
                self.parseNearbyCities(soup.find('section',
                                                 {'class': 'nearby-cities'}))
                for res in Results.endpoints:
                    """ we should strip the ?page param from the res.url"""
                    if settings['base_url']+res.endpoint == page.url:
                        print(res.endpoint)
                        res.pagination = self.parsePagination(
                            soup.find('span', {'class': 'showing-count'})
                            )
                '''
                the find_nearby_cities() will parse nearby cities
                and pagination for each city
                and return them in a new dictionary
                '''
                info_list = soup.find_all('div', {"class": "info"})
                for item_index, item in enumerate(info_list):
                    '''
                    call instance of class business and assign soup content
                    to instance attributes
                    the class will be responsible for cleaning the parsed data
                    '''
                    yellowpage = Yellowpage(
                        item.find('div', {'class': 'rating'}),  # rating
                    )
                    foursquare = Foursquare(
                        item.find('div',
                                  {'class': 'ratings'}),  # foursquare_rating
                    )
                    tripadvisor = Tripadvisor(
                        item.find('div', {'class': 'ratings'}),  # tripadvisor
                    )
                    access = Access(
                        item.find('div',
                              {'class': 'open-status'}),  # open_status
                        item.find('a',
                                {'class': 'track-visit-website',
                               'href': True}),  # website
                        item.find('a', {'class': 'order-online',
                                    'href': True}),  # order_online
                        )
                    business = Business(
                            item.find('a', {'class': 'business-name'}),  # name
                            item.find('div',
                                  {'class': 'price-range'}),  # price_range
                            item.find('div', {'class': 'number'}),
                            item.find('div', {'class': 'locality'}),  # locality
                            item.find_all("div",
                                      {"class": "categories"}),  # categories
                            item.find_all("div",
                                      {"class": "amenities-info"}
                                      ),  # amenities
                        )
                    record = [
                        access.get_access(),
                        business.get_business(),
                        tripadvisor.get_tripadvisor(),
                        yellowpage.get_yellowpage(),
                        foursquare.get_foursquare()
                        ]
            else:
                print('parsing failed')
                continue
                #Queries.do_upsert(record)
