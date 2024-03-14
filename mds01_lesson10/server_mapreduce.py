import asyncio
import json
from collections import defaultdict


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
async def map_reduce(text):
    # Видалення знаків пунктуації
    words = text.split()

    # Паралельний Мапінг
    mapped_result = await asyncio.gather(*[map_function(word) for word in words])

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_result)

    reduced_result = await asyncio.gather(
        *[reduce_function(values) for values in shuffled_values]
    )
    return dict(reduced_result)


async def handler(reader, writer):
    connect = await reader.read(100)
    if connect == b"\x01":
        writer.write(b"Allowed")
        await writer.drain()
    else:
        writer.write(b"No data received.Close connection")
        writer.close()
        await writer.wait_closed()
        return

    # Читаємо дані від клієнту
    data = await reader.read(1000 * 1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received text from {addr}")

    # Пишемо відповідь
    words_counts = await map_reduce(message)
    print(f"Computed squares: {words_counts}")
    try:
        writer.write(json.dumps(words_counts).encode())
        await writer.drain()
    except json.JSONDecodeError:
        print("Invalid JSON")
        writer.write(json.dumps({"error": "Invalid data"}).encode())

    print("Closing connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handler, "127.0.0.1", 8888
    )
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    async with server:
        try:
            await server.serve_forever()
        except asyncio.exceptions.CancelledError:
            print("Server is shutting down...")
        finally:
            print("Closing server")
            server.close()
            await server.wait_closed()
            print("Server closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server has been shut down")
