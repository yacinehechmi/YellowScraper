import json


class Business:

    def __init__(self,
                 item_number,
                 name,
                 phone,
                 locality,
                 price_range,
                 open_status,
                 rating,
                 rating_count,
                 tripadvisor,
                 foursquare_rating,
                 categories,
                 amenities,
                 website,
                 order_online,
                 year_in_business,
                 ):

        self.item_number = item_number
        self.name = name
        self.phone = phone
        self.locality = locality
        self.price_range = price_range
        self.open_status = open_status
        self.rating = rating
        self.rating_count = rating_count
        self.tripadvisor = tripadvisor
        self.foursquare_rating = foursquare_rating
        self.categories = categories
        self.amenities = amenities
        self.website = website
        if self.locality is not None:
            self.city = self.locality.text[0:self.locality.text.find(',')]
            self.zip_code = \
                self.locality.text[self.locality.text.rindex(' ')+1:]
            self.state_code = \
                self.locality.text[self.locality.text.find(',') + 2:
                                   len(self.locality.text)
                                   - len(self.zip_code)-1]
        else:
            self.city = None
            self.zip_code = None
            self.state_code = None
        self.order_online = order_online
        self.year_in_business = year_in_business

    def get_name(self):
        if self.name is None:
            return None
        else:
            # replace characters to not break the sql query
            # pretty sure there is a better way to handle this
            return self.name.text.replace("'", "_", 1)

    def get_phone(self):
        if self.phone is None:
            return None
        else:
            return self.phone.text

    def get_locality(self):
        if self.locality is None:
            return None
        else:
            return self.locality.text

    def get_price_range(self):
        if self.price_range is None:
            return None
        else:
            return len(self.price_range.text)

    def get_open_status(self):
        if self.open_status is None:
            return None
        else:
            return self.open_status.text

    # j.find('div', {'class': 'ratings'}) will be something like "five half"
    # we want to take that and convert it into float rating
    def get_rating(self):
        if self.rating is None:
            return None
        else:
            stars = {
                1: 'one',
                2: 'two',
                3: 'three',
                4: 'four',
                5: 'five',
                0.5: 'half',
            }
            rate_sum = 0
            for x in stars:
                for i in range(1, len(self.rating['class'])):
                    if self.rating['class'][i] == stars[x]:
                        rate_sum += x
            return rate_sum

    def get_rating_count(self):
        if self.rating_count is None:
            return None
        else:
            return int(self.rating_count.text)

    def get_tripadvisor_rating(self):
        try:
            dict_tripadvisor = json.loads(self.tripadvisor['data-tripadvisor'])
            return float(dict_tripadvisor["rating"])
        except (TypeError, KeyError):
            return None

    def get_tripadvisor_rating_count(self):
        try:
            dict_tripadvisor = json.loads(self.tripadvisor['data-tripadvisor'])
            return int(dict_tripadvisor["count"])
        except (TypeError, KeyError):
            return None

    def get_foursquare_rating(self):
        try:
            return float(self.foursquare_rating['data-foursquare'])
        except (TypeError, KeyError):
            return None

    def get_amenities(self):
        if self.amenities is None or self.amenities == []:
            return None
        else:
            amenities_list = [amenity.text for amenities_list in self.amenities
                              for amenity in amenities_list.find_all('span')]
            return amenities_list

    def get_categories(self):
        if self.categories is None or self.categories == []:
            return None
        else:
            categories_list = [category.text for categories_list
                               in self.categories
                               for category in categories_list.find_all('a')]
        return categories_list

    def get_website(self):
        if self.website is None:
            return None
        else:
            return self.website['href']

    def get_order(self):
        if self.order_online is None:
            return None
        else:
            return self.order_online.text

    def get_year_in_business(self):
        if self.year_in_business is None:
            return None
        else:
            return self.year_in_business.text

    def get_tripadvisor_info(self):
        return (
                self.get_tripadvisor_rating(),
                self.get_tripadvisor_rating_count()
                )

    def get_foursquare_info(self):
        return (
                self.get_foursquare_rating(),
                )

    def get_yellowpages_info(self):
        return (
                self.get_rating(),
                self.get_rating_count()
                )

    def get_access_info(self):
        return (
                self.get_open_status(),
                self.get_website(),
                self.get_order()
                )

    def get_business_info(self):
        return (
                self.get_name(),
                self.get_phone(),
                self.get_price_range(),
                self.get_year_in_business(),
                self.get_amenities(),
                self.get_categories(),
                self.city,
                self.state_code,
                self.zip_code,
                )
