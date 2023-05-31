import psycopg2
import logging
from settings import settings
from sql.queries import queries
logger = logging.getLogger(__name__)


class Connect():
    def __init__(self, db=None):
        try:
            self.conn = psycopg2.connect(
                    host=settings['db_creds']['host'],
                    user=settings['db_creds']['user'],
                    database=db,
                    password=settings['db_creds']['pass'],
                    port=settings['db_creds']['port'],
                )
            with self.conn as conn:
                self.conn.autocommit = True
                self.cur = conn.cursor()
        except (Exception, psycopg2.OperationalError) as e:
            print(e)


class Queries():
    def upsert(self, records):
        self.db = settings['db_creds']['db']
        with self.conn as conn:
            cur = conn.cursor()
            #  run first query to insert business_info data
            # and get back the id of a record
            #  and use that id to proceed inserting to the other related tables
            cur.execute(queries['upsert_into_tables'][0], records[0])
            for record in records:
                try:
                    cur.execute(record.query, record)
                except (Exception, psycopg2.DatabaseError) as error:
                    logger.error(f'''DATABASE QUERY FAILED:
                     {record.query}{record} \n error: {error}''')

    def create_db(self):
        with Connect().cur as cur:
            try:
                cur.execute(queries['create_db'])
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'''DATABASE QUERY FAILED:
                    {queries['create_db']} \n error: {error}''')

    def create_tables(self):
        with Connect(settings['db_creds']['database']).cur as cur:
            try:
                cur.execute(queries['create_tables'])
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f'''DATABASE QUERY FAILED
            {queries['create_tables']} \n error: {error}''')
