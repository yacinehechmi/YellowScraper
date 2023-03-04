other = "zoozlo"
cities = {"soukra": False, "bouficha": False}
index = 0

while index < len(cities) - 1:

    print(cities)
    if other not in cities.keys():
        cities.update({other: False})

    index += 1
print(cities)
