import asyncio
import logging

from aiopath import AsyncPath
from aiofile import async_open

logging.basicConfig(level=logging.DEBUG, format="%(processName)s %(message)s")


async def producer(file: AsyncPath, q: asyncio.Queue):
    async with async_open(file, "r", encoding="utf-8") as f:
        data = []
        async for line in f:
            data.append(str(line))
        await q.put((file, "".join(data)))


async def consumer(queue: asyncio.Queue):
    async with async_open("main.js", "w", encoding="utf-8") as f:
        while True:
            file, blob = await queue.get()
            await f.write(f"{blob}\n")
            queue.task_done()


async def main():
    files_for_reading = asyncio.Queue()

    list_files = AsyncPath(".").joinpath("files").glob("*.js")
    producers = [asyncio.create_task(producer(file, files_for_reading)) async for file in list_files]
    consumer_task = asyncio.create_task(consumer(files_for_reading))

    await asyncio.gather(*producers)
    await files_for_reading.join()
    consumer_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
