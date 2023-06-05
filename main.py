import asyncio
from utils.Parse import Parse
from utils.Fetch import Fetch
from utils.dataclasses import Results, Result
from settings import DEFAULT_CITIES, DEFAULT_PAGINATION


def main():
    [Results.updateEndpoints(Result(city, 0, 0, DEFAULT_PAGINATION))
     for city in DEFAULT_CITIES]
    while True:
        new_endpoints = Results.getEndpoints()
        if new_endpoints:
            fetchResults = Fetch(new_endpoints)
            results = asyncio.run(fetchResults.fetch())
            Parse(results).parseContentAndStore()
        else:
            False


if __name__ == "__main__":
    main()
