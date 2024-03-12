import asyncio


async def baz():
    # await asyncio.sleep(0)
    return 'Baz'


async def main():
    result = await baz()
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
