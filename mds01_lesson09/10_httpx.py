import asyncio

import httpx
from icecream import ic


class HttpError(Exception):
    ...


async def request(url):
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            raise HttpError(f"Request error: {res.status_code} to {url}")


async def main():
    try:
        data = await request("https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")
        return data
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    c = asyncio.run(main())
    ic(c)
