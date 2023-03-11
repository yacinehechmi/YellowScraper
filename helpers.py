import pandas as pd
import os
import datetime as dt


def find_nearby_cities(nearby_cities, cities):
    if nearby_cities is not None:
        for nearby_city in nearby_cities:
            for name in nearby_city.find_all('a', {'href': True}):
                if name['href'] not in [item for subdict in cities for item in subdict]:
                    cities.append({name['href']: False})
        return True
    else:
        return False

# work in progress for this script please note that it's not used in the main script
# fixing to same length the categories and amenities lists


# dictionary to dataframe to csv
def dict_to_csv(data_dict, csv_file_name):
    dir_path = os.getcwd()
    # if file exist add values without headers
    if os.path.isfile(dir_path + "/" + f"{csv_file_name}"):
        df = pd.DataFrame([data_dict])
        df['timestamp'] = dt.datetime.now()
        df.to_csv(csv_file_name, mode='a', index=False, header=False)
    else:
        # create file and add values with headers
        df = pd.DataFrame([data_dict])
        df['timestamp'] = dt.datetime.now()
        df.to_csv(csv_file_name, index=False, mode='a')


# remove duplicates from csv
def clean_csv(csv_file_name):
    dir_path = os.getcwd()
    df = pd.read_csv(csv_file_name)
    df_clean = df.drop_duplicates(subset=['name'])
    os.remove(dir_path + "/" + f"{csv_file_name}")
    df_clean.to_csv(csv_file_name, mode='a', index=False)
