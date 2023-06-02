from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
''' if you wish to try this program with the default urls list and pagination
make sure to set default_settings paramater to True '''
settings = {
    'default_settings': False,
    'defualt_cities': [
        "/los-angeles-ca/restaurants"
            ],
    'default_pagination': 3,
    'csv_file_name': 'business.csv',
    'base_url': 'https://www.yellowpages.com',
    'db_creds': {
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT'),
        'pass': os.getenv('PG_PASS'),
        'user': os.getenv('PG_USER'),
        'database': os.getenv('DB')
    }
}
''' [
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
"/bronx-ny/restaurants" ] '''
