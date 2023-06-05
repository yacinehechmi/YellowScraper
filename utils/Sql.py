import psycopg2
from settings import settings
from sql.queries import queries

import logging
logger = logging
logger.basicConfig(level=logging.ERROR, filename='logs/queries.log',
                   format='[%(asctime)s] %(levelname)s:%(message)s')


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
            logger.error(e)


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
                    except (Exception, psycopg2.DatabaseError) as e:
                        logger.error(e)
            except (Exception, psycopg2.DatabaseError) as e:
                logger.error(e)

    def create_db(self):
        with Connect().cur as cur:
            try:
                cur.execute(queries['create_db'])
            except (Exception, psycopg2.DatabaseError) as e:
                logger.error(e)

    def create_tables(self):
        with Connect(settings['db_creds']['database']).cur as cur:
            try:
                cur.execute(queries['create_tables'])
            except (Exception, psycopg2.DatabaseError) as e:
                logger.error(e)
