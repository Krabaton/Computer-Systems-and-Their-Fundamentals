import asyncio
import platform

import aiohttp
from icecream import ic

class HttpError(Exception):
    ...


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HttpError(f"Request error: {response.status} to {url}")

        except (aiohttp.ClientConnectionError, aiohttp.InvalidURL) as err:
            raise HttpError(f"Connection error: {err} to {url}")


async def main():
    try:
        data = await request("https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")
        return data
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    c = asyncio.run(main())
    ic(c)

