from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
''' if you wish to try this program with the default urls list and then
let the program figure out the pagination and other endpoints not included
here you can set the default_settings to False
just be aware that the server might block requests from your ip address
considuring the amount, please do not abuse '''

DEFAULT_SETTINGS = True
DEFAULT_PAGINATION = 3
CSV_FILE_NAME = "yellowpages_restaurants.csv"
DEFAULT_CITIES = [
        "/los-angeles-ca/restaurants",
        "/miami-fl/restaurants",
        "/phoenix-az/restaurants",
        "/las-vegas-nv/restaurants",
        "/san-antonio-tx/restaurants",
        "/houston-tx/restaurants",
        "/chicago-il/restaurants",
        "/dallas-tx/restaurants",
        "/orlando-fl/restaurants",
        "/philadelphia-pa/restaurants",
        "/atlanta-ga/restaurants",
        "/oklahoma-city-ok/restaurants",
        "/indianapolis-in/restaurants",
        "/memphis-tn/restaurants",
        "/charlotte-nc/restaurants",
        "/louisville-ky/restaurants",
        "/jacksonville-fl/restaurants",
        "/el-paso-tx/restaurants",
        "/detroit-mi/restaurants",
        "/denver-co/restaurants",
        "/milwaukee-wi/restaurants",
        "/columbus-oh/restaurants",
        "/saint-louis-mo/restaurants",
        "/fort-worth-tx/restaurants",
        "/kansas-city-mo/restaurants",
        "/albuquerque-nm/restaurants",
        "/baltimore-md/restaurants",
        "/baton-rouge-la/restaurants",
        "/sacramento-ca/restaurants",
        "/fresno-ca/restaurants",
        "/austin-tx/restaurants",
        "/nashville-tn/restaurants",
        "/tulsa-ok/restaurants",
        "/tucson-az/restaurants",
        "/tampa-fl/restaurants",
        "/birmingham-al/restaurants",
        "/bakersfield-ca/restaurants",
        "/new-york-ny/restaurants",
        "/cleveland-oh/restaurants",
        "/brooklyn-ny/restaurants",
        "/san-diego-ca/restaurants",
        "/corpus-christi-tx/restaurants",
        "/salt-lake-city-ut/restaurants",
        "/cincinnati-oh/restaurants",
        "/fort-lauderdale-fl/restaurants",
        "/new-orleans-la/restaurants",
        "/knoxville-tn/restaurants",
        "/columbia-sc/restaurants",
        "/bronx-ny/restaurants"
        ]
BASE_URL = "https://www.yellowpages.com"
DB_CREDENTIALS = {
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT'),
        'pass': os.getenv('PG_PASS'),
        'user': os.getenv('PG_USER'),
        'database': os.getenv('DB')
    }
