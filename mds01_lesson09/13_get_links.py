import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests
from icecream import ic
from requests.exceptions import InvalidSchema, MissingSchema, SSLError

from timing import async_timed

urls = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
    "https://www.greenteapress.com/",
    "https://inventwithpython.com/",
    "https://www.artima.com/",
    "https://www.stackoverflow.com/",
    "https://www.python.org/",
    "https://realpython.com/",
    "https://www.python.org/asdwf",
    # "test"
]


def get_preview(url):
    try:
        txt = requests.get(url).text[:25]
        return url, txt
    except (InvalidSchema, MissingSchema, SSLError) as err:
        ic(err)


@async_timed(name="requests")
async def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_running_loop()
        futures = [loop.run_in_executor(executor, get_preview, url) for url in urls]
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        print(f"Done: {done}")
        print(f"Pending: {pending}")
        [f.cancel() for f in pending]

        return done


if __name__ == "__main__":
    result = asyncio.run(main())
    [print(r) for r in result]
