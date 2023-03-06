

def find_nearby_cities(nearby_cities, cities):
    if nearby_cities is not None:
        for nearby_city in nearby_cities:
            for name in nearby_city.find_all('a', {'href': True}):
                if name['href'] not in [item.keys for item in cities]:
                    cities.append({name['href']: False})
