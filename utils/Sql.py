import psycopg2
from settings import DB_CREDENTIALS
from sql.queries import queries
from utils.logger import setup_logger

queries_logger = setup_logger('queries_logger', 'logs/queries.log')


class Connect():
    def __init__(self, db=None):
        try:
            self.conn = psycopg2.connect(
                    host=DB_CREDENTIALS['host'],
                    user=DB_CREDENTIALS['user'],
                    database=db,
                    password=DB_CREDENTIALS['pass'],
                    port=DB_CREDENTIALS['port'],
                )
            with self.conn as conn:
                self.conn.autocommit = True
                self.cur = conn.cursor()
        except (Exception, psycopg2.OperationalError) as e:
            queries_logger.error(e)


class Queries():
    def upsert(self, cur, record):
        rec, query = record[0]
        try:
            cur.execute(query, rec)
            id = cur.fetchone()[0]
            for rec in record[1:]:
                r, query = rec
                r += (id,)
                try:
                    cur.execute(query, r)
                except (Exception, psycopg2.DatabaseError) as e:
                    queries_logger.error(e)
        except (Exception, psycopg2.DatabaseError) as e:
            queries_logger.error(e)

    def iter_through_queries(self, records):
        with Connect(DB_CREDENTIALS['database']).cur as cur:
            list(map(lambda record: self.upsert(cur, record), records))

    def create_db(self):
        with Connect().cur as cur:
            try:
                cur.execute(queries['create_db'])
            except (Exception, psycopg2.DatabaseError) as e:
                queries_logger.error(e)

    def create_tables(self):
        with Connect(DB_CREDENTIALS['database']).cur as cur:
            try:
                cur.execute(queries['create_tables'])
            except (Exception, psycopg2.DatabaseError) as e:
                queries_logger.error(e)
