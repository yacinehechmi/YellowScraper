from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

settings = {
    "csv_file_name": 'busi.csv',
    "number_of_pages": 2,
    "cities": [{'/los-angeles-ca/retaurants': False}],
    "db_creds": {
        "host": os.getenv('HOST'),
        "port": os.getenv('PORT'),
        "pass": os.getenv('PG_PASS'),
        "user": os.getenv('PG_USER'),
        "db": os.getenv('DB'),
    },
}
