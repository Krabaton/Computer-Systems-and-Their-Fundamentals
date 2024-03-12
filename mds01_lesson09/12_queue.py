import asyncio
from random import randint


async def producer(queue: asyncio.Queue):
    num = randint(0, 1000)
    await asyncio.sleep(0.1)
    await queue.put(num)


async def consumer(queue: asyncio.Queue):
    while True:
        num = await queue.get()
        print(f"Consumed {num}: {num**2}")
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    producers = [asyncio.create_task(producer(queue)) for _ in range(100)]
    consumers = [asyncio.create_task(consumer(queue)) for _ in range(5)]
    await asyncio.gather(*producers)
    await queue.join()
    [task.cancel() for task in consumers]


if __name__ == "__main__":
    asyncio.run(main())
