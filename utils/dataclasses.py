from dataclasses import dataclass, field
from sql.queries import queries
import json


upserts = queries['upsert_into_tables']


@dataclass()
class Result():
    endpoint: str = ""
    default_pagination: bool = True
    pages_scraped: int = 0
    pages_stored: int = 0
    is_scraped: bool = False
    is_stored: bool = False
    total_pages: int = 3

    def updateStored(self, stored):
        self.pages_stored += stored

    def updateScraped(self, scraped):
        self.pages_scraped += scraped


@dataclass()
class Results():
    endpoints = []

    @classmethod
    def updateEndpoints(cls, endpoint):
        cls.endpoints.append(endpoint)

    @classmethod
    def getEndpointsNames(cls):
        endpoints_list = []
        for endpoint in cls.endpoints:
            endpoints_list.append(endpoint.endpoint)
        return endpoints_list

    @classmethod
    def getEndpoints(cls):
        return cls.endpoints

    @classmethod
    def getNewEndpoints(cls):
        return [city for city in cls.endpoints if
                city.total_pages != city.pages_scraped]


@dataclass()
class Business():
    name: str
    price_range: int
    year_in_business: int
    locality: str = field(default='')
    categories: list[int] = field(default_factory=list)
    amenities: list[int] = field(default_factory=list)
    city_name: str = field(init=False)
    zip_code: str = field(init=False)
    state_code: str = field(init=False)
    query: str = upserts[0]

    def __post_init__(self):
        # name
        if self.name:
            self.name = self.name.text.replace("'", "_", 1)
        else:
            self.name = None
        # zip_code, city_name, state_code
        if self.locality:
            self.city_name = self.locality.text[0:self.locality.text.find(',')]
            self.zip_code = self.locality.text[
                    self.locality.text.rindex(' ')+1:
                    ]
            self.state_code = \
                self.locality.text[
                                   self.locality.text.find(',')+2:
                                   len(self.locality.text) -
                                   len(self.zip_code)-1
                                   ]
        else:
            self.city_name = None
            self.state_code = None
            self.zip_code = None
        # price_range
        if self.price_range:
            self.price_range = len(self.price_range)
        else:
            self.price_range = None
        # year_in_business
        if self.year_in_business:
            self.year_in_business = int(self.year_in_business.text)
        else:
            self.year_in_business = None
        # amenties
        if self.categories:
            self.categories = [category for categories_list in
                               self.categories for category in
                               categories_list]
        else:
            self.categories = None
        # categories
        if self.amenities:
            self.amenities = [amenity for amenities_list in
                              self.amenities for amenity in
                              amenities_list if amenity.text]
        else:
            self.amenities = None

    def get_business(self):
        return (
                self.name,
                self.price_range,
                self.year_in_business,
                self.amenities,
                self.categories,
                self.city_name,
                self.state_code,
                self.zip_code
                )


@dataclass()
class Access():
    open_status: str
    website: str
    order_online: bool
    query: str = upserts[1]

    def __post_init__(self):
        # open_status
        if self.open_status:
            self.open_status = self.open_status.text
        else:
            self.open_status = None
        # website
        if self.website:
            self.website = self.website['href']
        else:
            self.website = None
        # order_online
        if self.order_online:
            self.order_online = self.order_online.text
        else:
            self.order_online = None

    def get_access(self):
        return (
                self.open_status,
                self.website,
                self.order_online
                )


@dataclass()
class Tripadvisor():
    tripadvisor_rating: float = None
    tripadvisor_rating_count: int = None
    tripadvisor: dict = field(default_factory=dict, repr=False)
    query: str = upserts[2]

    def __post_init__(self):
        if self.tripadvisor:
            try:
                trip_dict = json.loads(self.tripadvisor['data-tripadvisor'])
                self.tripadvisor_rating_count = int(trip_dict['count'])
                self.tripadvisor_rating = float(trip_dict['rating'])
            except (TypeError, KeyError):
                pass
        else:
            self.tripadvisor_rating_count = 0
            self.tripadvisor_rating = 0

    def get_tripadvisor(self):
        return (
                self.tripadvisor_rating_count,
                self.tripadvisor_rating
                )


@dataclass()
class Yellowpage():
    yellowpage_rating: float = field(init=False)
    yellowpage_rating_count: int = field(init=False)
    yellowpage: dict = field(default_factory=dict)
    query: str = upserts[3]

    def __post_init__(self):
        if self.yellowpage:
            if self.yellowpage.find('span', {'class': 'count'}):
                rating_count = \
                    self.yellowpage.find('span', {'class': 'count'}).text
                self.yellowpage_rating_count = rating_count.replace('(', '')
                self.yellowpage_rating_count =  \
                    self.yellowpage_rating_count.replace(')', '')
                self.yellowpage_rating_count =  \
                    int(self.yellowpage_rating_count)
            else:
                self.yellowpage_rating_count = 0
            if self.yellowpage.find('div', {'class': 'result-rating'}):
                rating = self.yellowpage.find(
                        'div', {'class': 'result-rating'}
                        )['class']
                stars = {
                        1: 'one',
                        2: 'two',
                        3: 'three',
                        4: 'four',
                        5: 'five',
                        0.5: 'half'
                        }
                rate_sum = 0
                for float_num, star in stars.items():
                    for rate in rating[1:]:
                        if rate == star:
                            rate_sum += float_num
                self.yellowpage_rating = float(rate_sum)
            else:
                self.yellowpage_rating = 0
        else:
            self.yellowpage_rating = 0
            self.yellowpage_rating_count = 0

    def get_yellowpage(self):
        return (
                self.yellowpage_rating,
                self.yellowpage_rating_count
                )


@dataclass()
class Foursquare():
    foursquare: dict = field(default_factory=dict)
    foursquare_rating: float = field(init=False)
    query: str = upserts[4]

    def __post_init__(self):
        if self.foursquare:
            try:
                if self.foursquare['data-foursquare']:
                    self.foursquare_rating = float(
                        self.foursquare['data-foursquare']
                        )
            except (TypeError, KeyError):
                self.foursquare_rating = 0
        else:
            self.foursquare_rating = 0

    def get_foursquare(self):
        return (self.foursquare_rating,)
