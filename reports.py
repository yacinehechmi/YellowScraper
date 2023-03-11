from sqlalchemy import create_engine
from Settings import settings, queries
import pandas as pd

host = settings['db_creds']['host']
database = 'yellowpages'
user = settings['db_creds']['user']
password = settings['db_creds']['pass']
port = settings['db_creds']['port']
db = settings['db_creds']['db']
#  what i need to do:
# create dataframe
# use dataframe to create csv
# use dataframe to create visualizations


def main():
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
    # add an empty dict here
    # add empty dataframe
    result_proxy = engine.execute(queries['select'])
    results = result_proxy.fetchall()
    df = pd.DataFrame(results, columns=result_proxy.keys())
    df.to_csv('data/sample_data.csv')
    print(df.info())

if __name__ == "__main__":
    main()