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
        with Connect(settings['db_creds']['database']).cur as cur:
            rec, query = records[0]
            try:
                cur.execute(query, rec)
                id = cur.fetchone()[0]
                for record in records[1:]:
                    rec, query = record
                    rec += (id,)
                    try:
                        cur.execute(query, rec)
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(f"{error} \n in query {query} \n record {rec}")
                        logger.error(f'''DATABASE QUERY FAILED:
                     {query}{rec} \n error: {error}''')
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"{error} \n in query {query} \n record {rec}")
                logger.error(f'''DATABASE QUERY FAILED:
                   {query}{rec} \n error: {error}''')

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
