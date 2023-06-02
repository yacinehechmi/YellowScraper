# YellowScraper-v1
- This project is part of my Data Engineering studies, This is a python scraper that retrieves restaurant listings data from yellowpages.com and stores it in a postgres database
The scraper fetches data based on a dictionary of city(s) and the number of page(s) requested for each city, it can also discover nearby cities by scraping the nearby cities section.

- The program is devided into two main categories of classes:
  1. data classes(check utils.dataclasses):
  These are responsible for storing and transforming the data to the appropriate format
  2. behavior classes (check utils):
  These are responsible for the logic or the behavior of a particular part of the program
    - Fetch for asyncrounsly requesting yellowpages.com server for html data
    - Parse for parsing the html data and passing it to the dataclasses
    - Queries for different database communications that are done in order to store the data in the database
  

## Prerequisites
- Python 3.x
- Conda
- Postgresql server

## To run this project
1) Clone the repo `git clone https://github.com/yacine717/YellowScraper`
2) Create conda environment `conda env create --name my_project --file environment.yml`
3) Activate conda environment `conda activate my_project` 
4) Run to create database and database tables `python3 init_sql.py`
5) Run the scraper `python3 main.py`

## Database model
The data then is stored in a normalized form to avoid data redundancy in the following tables
its represented as dataclasses in the program check `dataclasses.py`.
- Business_info:
  - Business_id, Bigserial, PrimaryKey
  - Name, Varchar
  - Phone, Varchar
  - Price_range, Int
  - Categories, Array of Text
  - Amenities, Array of Text
  - Year_in_business, Int
  - City_code, Varchar
  - City_name, Varchar
  - Zip_code, Varchar
  - Last_update, datetime
- Foursquare_info:
  - Business_id, bigint, ForiegnKey
  - Rating, Float
- Access_info:
  - Business_id, bigint, ForiegnKey
  - Open_status, Varchar
  - Website, Varchar
  - Order_online Varchar
- Tripadvisor_info:
  - Business_id, bigint, ForiegnKey
  - Rating, Float
  - Rating_count, Int
- Yellowpage_info:
  - Business_id, bigint, ForiegnKey
  - Rating, Float
  - Rating_count, Int

![Database Diagram](assets/database_model.png)

## TODO
  - Fix logging
  - Fix Fetch Exception handling
  - Add a Dockerfile

## Future Goals
  - Planning to create a second version of this project on airflow.

## Notes
- If you encounter any issues, please create a new issue in the repository.

## Acknowledgments
Special thanks to my fellow engineers at the dataGarage discord community who contributed valuable insights that helped in the making of this project.
