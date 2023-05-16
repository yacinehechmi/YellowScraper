from bs4 import BeautifulSoup as bs


def find_pagination(pagination):
    if pagination is not None:
        print(pagination.find('span'))
        pag_str = pagination.find('span')
        if pag_str:
            x = slice(pag_str.find('-')+1, pag_str.rfind('o')-1)
            y = slice(pag_str.rfind(' ')+1, len(pag_str))
            return int(int(pag_str[y])/int(pag_str[x]))
    else:
        return None


def find_nearby_cities(nearby_cities, cities):
    if nearby_cities is not None:
        for nearby_city in nearby_cities:
            for name in nearby_city.find_all('a', {'href': True}):
                if name['href'] not in [city for city in cities]:
                    cities.append(name['href'])
    else:
        return None


def build_cities_list(results, cities):
    for page in results:
        soup = bs(page)
        print(cities)
        print(find_pagination(soup.find('div', {'class': 'pagination'})))
        print('---')
        find_nearby_cities(soup.find('section', {'class': 'nearby-cities'}), cities)
    return cities
        
