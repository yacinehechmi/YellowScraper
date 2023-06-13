import asyncio
from utils.Parse import Parse
from utils.Fetch import Fetch
from utils.dataclasses import Results, Result
from settings import DEFAULT_CITIES, DEFAULT_PAGINATION


def main(new_results: list = None) -> None:
    if new_results is None:
        exit()
    else:
        results = asyncio.run(Fetch().fetch(new_results))
        list(map(lambda result: Parse().parse_content_and_store(result)
                 if result else None,
                 results))
        main(Results.get_results())


if __name__ == "__main__":
    [Results.set_results(Result(city, 0, DEFAULT_PAGINATION))
     for city in DEFAULT_CITIES]
    main(Results.get_results())
