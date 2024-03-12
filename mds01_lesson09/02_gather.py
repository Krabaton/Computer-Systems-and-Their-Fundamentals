import asyncio
from time import sleep, time

from faker import Faker

fake = Faker("uk-UA")
fake.seed_instance(42)


def get_user_from_db(user_id: int):
    sleep(0.5)  # імітація завантаження з бази
    return {"id": user_id, "username": fake.name(), "email": fake.email()}


async def async_get_user_from_db(user_id: int):
    await asyncio.sleep(0.5)  # імітація завантаження з бази
    return {"id": user_id, "username": fake.name(), "email": fake.email()}


async def main():
    users = []
    for i in range(1, 4):
        users.append(async_get_user_from_db(i))
    r = await asyncio.gather(*users)  # await asyncio.gather(async_get_user_from_db(1), async_get_user_from_db(2), ...)
    return r

# async def main():
#     users = []
#     for i in range(1, 4):
#         users.append(await async_get_user_from_db(i))
#     # r = await asyncio.gather(*users)  # await asyncio.gather(async_get_user_from_db(1), async_get_user_from_db(2), ...)
#     return users

if __name__ == "__main__":
    start = time()
    for i in range(1, 4):
        u = get_user_from_db(i)
        print(u)
    print(time() - start)

    start = time()
    u = asyncio.run(main())
    print(u)
    print(time() - start)
