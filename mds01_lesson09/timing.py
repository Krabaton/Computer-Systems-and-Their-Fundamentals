from functools import wraps
from time import time


def async_timed(*, name: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time()
            if name:
                print(f"{name} started")
            try:
                return await func(*args, **kwargs)
            finally:
                print(f"{name} finished in {time() - start:.2f} sec")

        return wrapper

    return decorator
