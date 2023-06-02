import logging
import asyncio
from utils.Parse import Parse
from utils.Fetch import Fetch
from utils.dataclasses import Results, Result
from settings import settings


def main():
    [Results.updateEndpoints(Result(city, 0, 0, 3))
     for city in settings['defualt_cities']]
    while True:
        new_endpoints = Results.getEndpoints()
        if new_endpoints:
            fetchResults = Fetch(new_endpoints)
            results = asyncio.run(fetchResults.fetch())
            Parse(results).parseContentAndStore()
            
        else:
            False

    print('end')


if __name__ == "__main__":
    logger = logging
    logger.basicConfig(level=logging.ERROR, filename='logs/scraper.log',
                       format='[%(asctime)s] %(levelname)s:%(message)s')
    main()
