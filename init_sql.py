import logging
from parameters import config
from sql import create_db, create_tables

def main():
    create_db()
    create_tables(config['db'])

if __name__ == '__main__':
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='init_sql.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
