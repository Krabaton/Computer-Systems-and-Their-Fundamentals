#!/usr/bin/env python

import asyncio

import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK


class WSServer:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        print(f"Client {ws.name}:{ws.remote_address} joined")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        print(f"Client {ws.name}:{ws.remote_address} diconnected")  # noqa

    async def broadcast(self, message: str):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handler(self, websocket: WebSocketServerProtocol):
        await self.register(websocket)
        try:
            await self.distribute(websocket)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(websocket)

    async def distribute(self, websocket: WebSocketServerProtocol):
        async for message in websocket:
            if message == "ping":
                await websocket.send("pong")
            elif message == "Hello server":
                await websocket.send(f"Hello {websocket.name}")
            else:
                await self.broadcast(f"{websocket.name}: {message}")


async def main():
    server = WSServer()
    async with websockets.serve(server.handler, "", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
