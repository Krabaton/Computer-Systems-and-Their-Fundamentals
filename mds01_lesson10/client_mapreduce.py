import asyncio
import json
import string

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


async def send_ping(writer):
    print("Sending ping")
    writer.write(b"\x01")
    await writer.drain()


async def send_text(writer, text):
    print("Sending data")
    writer.write(remove_punctuation(text).encode())
    await writer.drain()


async def received(reader, chunck_size=100):
    data = await reader.read(chunck_size)
    print(f"Recieved data: {data}")
    return data


async def main(url):
    result = None
    server = "127.0.0.1"
    port = 8888
    print(f"Get text from {url}")
    text = await get_text(url)
    reader, writer = await asyncio.open_connection(server, port)
    await send_ping(writer)
    response = await received(reader)
    if response == b"Allowed":
        await send_text(writer, text)
        result = await received(reader, 10*1024)

    print("Closing connection")
    writer.close()
    await writer.wait_closed()
    return result

if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    r = asyncio.run(main(url))
    print(r.decode())
