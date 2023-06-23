from __future__ import annotations

from typing import Any

import asyncio

from pickle import dumps
from uuid import UUID

from websockets.server import WebSocketServerProtocol, serve

from .common import avaliable_cloudable


connections: dict[int, Connection] = {}


class Connection:
    def __init__(
        self, ws: WebSocketServerProtocol,
        loop: asyncio.AbstractEventLoop | None = None
    ) -> None:
        self.loop = loop or asyncio.get_running_loop()
        self._ws = ws
        self.queue = asyncio.Queue[dict[str, Any]]()
        self.id = UUID().int
        self.fps: None | int = None
        self.interval = 0.
        self.components = []
        for raw_component in avaliable_cloudable:
            c = raw_component()
            c._connection = self
            self.components.append(c)

    async def start(self) -> None:
        # FPSを受け取る。
        raw_fps = await websocket.recv()
        assert isinstance(raw_fps, bytes)
        self.fps = int.from_bytes(raw_fps)
        self.interval = 1 / self.fps

        # 通信を始める。
        self.loop.create_task(self._process_queue())

        while True:
            await asyncio.sleep(self.interval)
            for component in self.components:
                component.update()

    async def _process_queue(self) -> None:
        while True:
            await self._ws.send(dumps(await self.queue.get()))


def run() -> None:
    asyncio.run(main())


async def on_connect(websocket: WebSocketServerProtocol):
    c = Connection(websocket)
    connections[c.id] = c

    await c.start()

async def main():
    async with serve(on_connect, "localhost", 8765):
        await asyncio.Future()