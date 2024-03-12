import asyncio
import random


async def ping(signal):
    print(f"ping {signal}")


async def pong(signal):
    print(f"pong {signal}")


async def main():
    while True:
        await asyncio.sleep(1)
        await ping(random.randint(1, 10))
        await pong(random.randint(1, 10))


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.create_task(ping('!!!!'))
    loop.run_forever()
