import string
import asyncio
from collections import defaultdict

import httpx


async def get_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None


# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


async def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


async def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
async def map_reduce(url):
    # Видалення знаків пунктуації
    text = await get_text(url)
    text = remove_punctuation(text)
    words = text.split()

    # Паралельний Мапінг
    mapped_result = await asyncio.gather(*[map_function(word) for word in words])

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_result)

    reduced_result = await asyncio.gather(
        *[reduce_function(values) for values in shuffled_values]
    )
    return dict(reduced_result)


if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    result = asyncio.run(map_reduce(url))
    print(result)
