from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

settings = {
    'csv_file_name': 'business.csv',
    'pagination': 3,
    'cities': ['/los-angeles-ca/retaurants'],
    'db_creds': {
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT'),
        'pass': os.getenv('PG_PASS'),
        'user': os.getenv('PG_USER'),
        'db': os.getenv('DB'),
    },
}
