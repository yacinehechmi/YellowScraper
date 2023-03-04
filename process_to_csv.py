import pandas as pd
import os
import datetime as dt


# fixing to same length the categories and amenities lists
def lists_to_same_length(data_dict):
    if len(data_dict['categories']) > len(data_dict['amenities']):
        data_dict['amenities'] += (len(data_dict['categories']) - len(data_dict['amenities'])) * [""]
    elif len(data_dict['amenities']) > len(data_dict['categories']):
        data_dict['categories'] += (len(data_dict['amenities']) - len(data_dict['categories'])) * [""]


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


# writing the data dictionary to csv
def write_to_csv(data_dict, csv_file_name):
    # check if length of amenities and categories lists are the same if not add empty array until they are the same
    lists_to_same_length(data_dict)
    # write dictionary to dataframe and store to csv
    dict_to_csv(data_dict, csv_file_name)


# remove duplicates from csv
def clean_csv(csv_file_name):
    dir_path = os.getcwd()
    df = pd.read_csv(csv_file_name)
    df_clean = df.drop_duplicates(subset=['name'])
    os.remove(dir_path + "/" + f"{csv_file_name}")
    df_clean.to_csv(csv_file_name, mode='a', index=False)
