import asyncio
import json


async def send_ping(writer):
    print("Sending ping")
    writer.write(b"\x01")
    await writer.drain()


async def send_data(writer, numbers):
    print("Sending data")
    writer.write(json.dumps(numbers).encode())
    await writer.drain()


async def received(reader, chunck_size=100):
    data = await reader.read(chunck_size)
    print(f"Recieved data: {data}")
    return data


async def main(numbers):
    result = None
    server = "127.0.0.1"
    port = 8888
    reader, writer = await asyncio.open_connection(server, port)
    await send_ping(writer)
    response = await received(reader)
    if response == b"Allowed":
        await send_data(writer, numbers)
        result = await received(reader, 10*1024)

    print("Closing connection")
    writer.close()
    await writer.wait_closed()
    return result

if __name__ == "__main__":
    r = asyncio.run(main([11, 22, 3, 4, 15, 16, 7, 8, 9, 10]))
    print(r.decode())
