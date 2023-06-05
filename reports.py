from sqlalchemy import create_engine
import pandas as pd
from sql.queries import queries
from settings import DB_CREDENTIALS, CSV_FILE_NAME


def main():
    engine = create_engine(f'''postgresql+psycopg2://
                           {DB_CREDENTIALS['user']}:{DB_CREDENTIALS['pass']}@{DB_CREDENTIALS['host']}:
                           {DB_CREDENTIALS['port']}/
                           {DB_CREDENTIALS['database']}''')
    # add an empty dict here
    # add empty dataframe
    results = engine.execute(queries['select'])
    res = results.fetchall()
    df = pd.DataFrame(res, columns=results.keys())
    df.to_csv(f'data/{CSV_FILE_NAME}')


if __name__ == "__main__":
    main()
