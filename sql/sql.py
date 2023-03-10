import psycopg2
import logging
import pandas as pd


# project modules
from Settings import settings
from sql.Queries import queries

logger = logging.getLogger(__name__)


def select_join(db):
    try:
        conn = psycopg2.connect(
            host=settings['db_creds']['host'],
            database=db,
            user=settings['db_creds']['user'],
            password=settings['db_creds']['pass'],
            port=settings['db_creds']['port'],
        )
        try:
            df = pd.read_sql(conn, queries['select'])
            print(df.info())
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {queries["upsert_into_tables"][0]} \n error: {error}')
            print(error)
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED: {error}')


def do_upsert(db, records=None):
    try:
        conn = psycopg2.connect(
            host=settings['db_creds']['host'],
            database=db,
            user=settings['db_creds']['user'],
            password=settings['db_creds']['pass'],
            port=settings['db_creds']['port'],
        )
        conn.autocommit = True
        logger.info('DATABASE CONNECTION SUCCESSFUL')
        cur = conn.cursor()
        #  run first query to insert business_info data and get back the id of a record
        #  and use that id to proceed inserting to the other related tables
        try:
            cur.execute(queries["upsert_into_tables"][0], records[0])
            business_id = cur.fetchone()[0]
            #  append the business_id to the rest of queries data
            records = [item+(business_id,) for item in records[1:]]
            records_index = 0
            for statement in queries["upsert_into_tables"][1:]:
                #  loop through the rest of statements and execute them
                try:
                    cur.execute(statement, records[records_index])
                    records_index += 1
                except (Exception, psycopg2.DatabaseError) as error:
                    logger.error(f'DATABASE QUERY FAILED: {statement} \n error: {error}')
                    print(error)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {queries["upsert_into_tables"][0]} \n error: {error}')
            print(error)
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED: {error}')


# Create database in postgresql server
def create_db():
    try:
        conn = psycopg2.connect(
            host=settings['db_creds']['host'],
            database="",
            user=settings['db_creds']['user'],
            password=settings['db_creds']['pass'],
            port=settings['db_creds']['port'],
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(queries["create_db_and_tables"][0])
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {queries["create_db_and_tables"][0]} \n error: {error}')
            print(error)
        conn.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED : {error}')


# Create tables business_info, access_info, yellowpages_info, tripadvisor_info, foursquare_info
def create_tables(db):
    try:
        conn = psycopg2.connect(
            host=settings['db_creds']['host'],
            database=db,
            user=settings['db_creds']['user'],
            password=settings['db_creds']['pass'],
            port=settings['db_creds']['port'],
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(queries["create_db_and_tables"][1])
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {queries["create_db_and_tables"][1]} \n error: {error}')
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED : {error}')

