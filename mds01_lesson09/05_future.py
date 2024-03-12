import asyncio

from faker import Faker

from timing import async_timed

fake = Faker("uk-UA")
fake.seed_instance(42)


# Awaitable -> coroutine
# Awaitable -> Future -> Task


async def get_user_from_db(user_id: int, future: asyncio.Future):
    await asyncio.sleep(0.5)  # імітація завантаження з бази
    future.set_result({"id": user_id, "username": fake.name(), "email": fake.email()})


def make_request(user_id: int):
    future = asyncio.Future()
    asyncio.create_task(get_user_from_db(user_id, future))
    return future


@async_timed(name="make_request")
async def main():
    """
    :param user_id:
    :return:
    """
    users = []
    for i in range(1, 4):
        users.append(make_request(i))
    print([u.done() for u in users])
    r = await asyncio.gather(*users)
    print([u.done() for u in users])
    return r


if __name__ == "__main__":
    u = asyncio.run(main())
    print(u)
