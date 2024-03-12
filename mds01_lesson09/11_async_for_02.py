import asyncio
from typing import Iterable, Awaitable

from faker import Faker

from timing import async_timed

fake = Faker("uk-UA")
fake.seed_instance(42)


async def get_user_from_db(user_id: int):
    await asyncio.sleep(0.5)  # імітація завантаження з бази
    return {"id": user_id, "username": fake.name(), "email": fake.email()}


async def get_users(user_ids: list[int]):
    return [get_user_from_db(user_id) for user_id in user_ids]


@async_timed(name="gather")
async def main(users):
    new_users = []
    for user in await users:
        new_users.append(user)
    r = await asyncio.gather(*new_users)
    return r


if __name__ == "__main__":
    u = asyncio.run(main(get_users([1, 2, 3])))
    print(u)
