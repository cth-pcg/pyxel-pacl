import asyncio
from uuid import UUID

from websockets.server import WebSocketServerProtocol, serve


connections: dict[int, "Connection"] = {}


class Connection:
    def __init__(self, ws: WebSocketServerProtocol):
        self._ws = ws
        self.queue = asyncio.Queue()
        self.id = UUID().int

    async def process_queue(self) -> None:
        while True:
            data = await self.queue.get()
            await self._ws.send(data)


def prepare() -> None:
    ...


async def on_connect(websocket: WebSocketServerProtocol):
    c = Connection(websocket)
    connections[c.id] = c

    raw_fps = await websocket.recv()
    assert isinstance(raw_fps, bytes)

    fps = int.from_bytes(raw_fps)
    await c.process_queue()

async def main():
    async with serve(on_connect, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())