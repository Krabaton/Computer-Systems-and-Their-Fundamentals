import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests

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
    "test"
]


def get_preview(url):
    txt = requests.get(url).text[:25]
    return url, txt


@async_timed(name="requests")
async def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_running_loop()
        futures = [loop.run_in_executor(executor, get_preview, url) for url in urls]
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result


if __name__ == "__main__":
    result = asyncio.run(main())
    result = [r for r in result if not isinstance(r, Exception)]
    [print(r) for r in result]
