import asyncio
import json


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
    data = await reader.read(10*1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message} from {addr}")

    # Пишемо відповідь
    try:
        numbers = json.loads(message)
        squares = await compute_squares(numbers)
        print(f"Computed squares: {squares}")
        writer.write(json.dumps(squares).encode())
        await writer.drain()
    except json.JSONDecodeError:
        print("Invalid JSON")
        writer.write(json.dumps({"error": "Invalid data"}).encode())

    print("Closing connection")
    writer.close()


async def compute_square(n):
    await asyncio.sleep(0)
    return n * n


async def compute_squares(numbers):
    return [await compute_square(x) for x in numbers]


async def main():
    server = await asyncio.start_server(
        handler, "127.0.0.1", 8888
    )
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
