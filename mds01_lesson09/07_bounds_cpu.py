import asyncio
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


async def ping(signal):
    print(f"ping {signal}")


async def worker():
    while True:
        await asyncio.sleep(1)
        await ping(random.randint(1, 10))


def calculate(counter: int):  # CPU bound
    init = counter
    while counter > 0:
        counter -= 1
    print(f"Completed operation {init}")
    return init


async def main():
    loop = asyncio.get_running_loop()
    task = loop.create_task(worker())  # noqa

    with ProcessPoolExecutor() as executor:
        futures = [
            loop.run_in_executor(executor, calculate, counter)
            for counter in [100_000_000, 120_000_000, 130_000_000]
        ]
        results = await asyncio.gather(*futures)
        task.cancel()
        return results


if __name__ == '__main__':
    asyncio.run(main())
