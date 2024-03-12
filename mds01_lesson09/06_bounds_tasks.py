import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def read_file(filename):  # IO bound
    with open(filename, 'r') as f:
        return f.read(100)


def calculate(power: int, p: int):  # CPU bound
    r = [i**power for i in range(10**p)]
    return sum(r)


async def main():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as executor:
        f = await loop.run_in_executor(executor, read_file, 'timing.py')
        print(f)

    with ProcessPoolExecutor() as executor:
        p = await loop.run_in_executor(executor, calculate, 2, 5)
        print(p)


if __name__ == '__main__':
    asyncio.run(main())
