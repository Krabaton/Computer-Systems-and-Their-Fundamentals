import asyncio
from time import sleep, time

from faker import Faker

fake = Faker("uk-UA")
fake.seed_instance(42)

# Awaitable -> coroutine
# Awaitable -> Future -> Task


async def get_user_from_db(user_id: int):
    await asyncio.sleep(0.5)  # імітація завантаження з бази
    return {"id": user_id, "username": fake.name(), "email": fake.email()}


async def main():
    users = []
    for i in range(1, 4):
        task = asyncio.create_task(get_user_from_db(i))
        users.append(task)
    r = await asyncio.gather(*users)  # await asyncio.gather(async_get_user_from_db(1), async_get_user_from_db(2), ...)
    return r


if __name__ == "__main__":
    start = time()
    u = asyncio.run(main())
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # u = loop.run_until_complete(main())
    print(u)
    print(time() - start)
