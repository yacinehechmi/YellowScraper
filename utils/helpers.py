def find_pagination(pagination):
    if pagination is not None:
        pag_str = pagination.find('span')
        if pag_str:
            x = slice(pag_str.find('-')+1, pag_str.rfind('o')-1)
            y = slice(pag_str.rfind(' ')+1, len(pag_str))
            return int(int(pag_str[y])/int(pag_str[x]))
    else:
        return None


def find_nearby_cities(nearby_cities, cities):
    new_cities = {}
    if nearby_cities is not None:
        for nearby_city in nearby_cities:
            for city in nearby_city.find_all('a', {'href': True}):
                if city['href'] not in [city for city in cities.keys()]:
                    new_cities.update({city['href']: False})
                    cities.update({city['href']: False})
    return new_cities
