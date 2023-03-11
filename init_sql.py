import logging
# project modules
from Settings import settings
from sql import create_db, create_tables

def main():
    create_db()
    create_tables(settings['db_creds']['db'])


if __name__ == '__main__':
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='logs/init_sql.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
