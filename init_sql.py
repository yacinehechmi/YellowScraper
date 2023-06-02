import logging
from utils.Sql import Queries


def main():
    p = Queries()
    p.create_db()
    p.create_tables()


if __name__ == '__main__':
    logger = logging
    logger.basicConfig(level=logging.INFO, filename='logs/init_sql.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
