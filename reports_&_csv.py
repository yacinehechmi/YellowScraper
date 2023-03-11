from sql import select_join
from sqlalchemy import create_engine

from Settings import settings, queries

host = settings['db_creds']['host']
database = 'yellowpages'
user = settings['db_creds']['user']
password = settings['db_creds']['pass']
port = settings['db_creds']['port']

#  what i need to do:
# create dataframe
# use dataframe to create csv
# use dataframe to create visualizations


def main():
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/yellowpages')

    result = engine.execute(queries['select'])
    for record in result:
        print(record)
if __name__ == "__main__":
    main()