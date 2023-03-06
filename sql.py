import psycopg2
from dotenv import load_dotenv
import os
from parameters import create_queries, upsert_into_tables
import logging
logger = logging.getLogger(__name__)
# set up the connection for given database name 'db' to a postgresql server
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def do_upsert(db, records=None):
    try:
        conn = psycopg2.connect(
            host='localhost',
            database=db,
            user='postgres',
            password='postgres',
            port='5432',
        )
        conn.autocommit = True
        logger.info('DATABASE CONNECTION SUCCESSFUL')
        cur = conn.cursor()
        try:
            #  run first query to insert business_info data and get back the id of a record
            #  and use that id to proceed inserting to the other related tables
            cur.execute(upsert_into_tables[0], records[0])
            business_id = cur.fetchone()[0]
            records = [item+(business_id,) for item in records[1:]]
            records_index = 0
            for statement in upsert_into_tables[1:]:
                try:
                    cur.execute(statement, records[records_index])
                    records_index += 1
                    logger.info(f' DATABASE QUERY SUCCESSFUL: {statement}')
                except (Exception, psycopg2.DatabaseError) as error:
                    logger.error(f'DATABASE QUERY FAILED: {statement} \n error: {error}')
                    print(error)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'DATABASE QUERY FAILED: {upsert_into_tables[0]} \n error: {error}')
            print(error)
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED : {error}')


# good
def create_db_and_tables(db):
    try:
        conn = psycopg2.connect(
            host='localhost',
            database=db,
            user='postgres',
            password='postgres',
            port='5432',
        )
        conn.autocommit = True
        logger.info('DATABASE CONNECTION SUCCESSFUL')
        cur = conn.cursor()
        if db:
            try:
                cur.execute(create_queries["create_tables"])
                print(create_queries["create_tables"])
                logger.info(f'DATABASE QUERY SUCCESSFUL: {create_queries["create_tables"]}')
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'DATABASE QUERY FAILED: {create_queries["create_tables"]} \n error: {error}')
                print(error)
        else:
            try:
                cur.execute(create_queries["create_db"])
                print(create_queries["create_db"])
                logger.info(f'DATABASE QUERY SUCCESSFUL: {create_queries["create_db"]}')
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'DATABASE QUERY FAILED: {create_queries["create_db"]} \n error: {error}')
                print(error)
            conn.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(f'DATABASE CONNECTION FAILED : {error}')