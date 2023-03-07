# yellow-scraper 
- This is a python scraper that retrieves restaurant listings data from yellowpages.com and stores it in a postgres database
The scraper take in as parameters the number of page(s) to fetch in each city, and a list of city(s) desired to be fetched
- The scraper can also discover nearby cities by scraping the nearby cities section.
## Prerequisites
- Python 3.x
- Conda
- postgresql server

## to run this project:
1) Clone the repo `git clone https://github.com/yacine717/YellowScraper`
2) Create conda environment `conda env create --name my_project --file environment.yml`
3) Activate conda environment `conda activate my_project` 
4) Run the script `python3 scraper.py`

## database diagram
the data is stored in a normalized for to avoid data redundancy in the following tables:
- Business_info:
  - business_id, Bigserial, PrimaryKey
  - Name, Varchar
  - Phone, Varchar
  - Price_range, Int
  - Categories, Array of Text
  - Amenities, Array of Text
  - Year_in_business, Int
  - City_code, Varchar
  - City_name, Varchar
  - Zip_code, Varchar
  - last_update, datetime
- Foursquare_info:
  - Business_id, bigint, ForiegnKey
  - Rating, Float
- Access_info
  - Business_id, bigint, ForiegnKey
  - Open_status, Varchar
  - Website, Varchar
  - Order_online Varchar
- Tripadvisor_info
  - Business_id, bigint, ForiegnKey
  - Rating, Float
  - Rating_count, Int
- Yellowpage_info
  - Business_id, bigint, ForiegnKey
  - Rating, Float
  - Rating_count, Int
  
![Database Diagram](/assets/database_model.png)
## Notes
- the csv processing part of this project is still in progress 
- if you encounter any issues while running the scraper, please create a new issue in the repository.

## Acknowledgments
Special thanks to my fellow engineers at the dataGarage discord community who helped in the making of this project.