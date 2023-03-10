import psycopg2
from dotenv import load_dotenv
import os
import logging
# project modules
from parameters import create_queries, upsert_into_tables

logger = logging.getLogger(__name__)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def do_upsert(db, records=None):
    try:
        conn = psycopg2.connect(
            host=os.getenv('HOST'),
            database=db,
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('HOST'),
        )
        conn.autocommit = True
        logger.info('DATABASE CONNECTION SUCCESSFUL')
        cur = conn.cursor()
        #  run first query to insert business_info data and get back the id of a record
        #  and use that id to proceed inserting to the other related tables
        try:
            cur.execute(upsert_into_tables[0], records[0])
            business_id = cur.fetchone()[0]
            #  append the business_id to the rest of queries data
            records = [item+(business_id,) for item in records[1:]]
            records_index = 0
            for statement in upsert_into_tables[1:]:
                #  loop through the rest of statements and execute them
                try:
                    cur.execute(statement, records[records_index])
                    records_index += 1
                except (Exception, psycopg2.DatabaseError) as error:
                    logger.error(f'DATABASE QUERY FAILED: {statement} \n error: {error}')
                    print(error)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {upsert_into_tables[0]} \n error: {error}')
            print(error)
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED: {error}')


# Create tables business_info, access_info, yellowpages_info, tripadvisor_info, foursquare_info
def create_tables(db):
    try:
        conn = psycopg2.connect(
            host=os.getenv('HOST'),
            database=db,
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('HOST'),
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(create_queries["create_tables"])
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {create_queries["create_tables"]} \n error: {error}')
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED : {error}')


# Create database in postgresql server
def create_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv('HOST'),
            database=os.getenv('DB'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('HOST'),
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(create_queries["create_db"])
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {create_queries["create_db"]} \n error: {error}')
            print(error)
        conn.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED : {error}')
