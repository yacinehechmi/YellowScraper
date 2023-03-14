def find_pagination(pagination):
    if pagination is not None:
        print(pagination.find('span'))
    else:
        print('no pagination')


def find_nearby_cities(nearby_cities, cities):
    if nearby_cities is not None:
        for nearby_city in nearby_cities:
            for name in nearby_city.find_all('a', {'href': True}):
                if name['href'] not in [item for subdict in cities for item in subdict]:
                    cities.append({name['href']: False})
        return True
    else:
        return False