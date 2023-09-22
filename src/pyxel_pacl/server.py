from __future__ import annotations

from typing import TYPE_CHECKING, Any
from asyncio import AbstractEventLoop, Future, Queue, get_running_loop, \
    run as arun, sleep

from pickle import dumps
from uuid import UUID

from websockets.server import WebSocketServerProtocol, serve

from .types_ import CloudableCore as AbcCloudableCore

if TYPE_CHECKING:
    from .common import Cloudable


connections = dict[int, "Connection"]()
avaliable_cloudable = list[type["Cloudable"]]()


class Connection:
    "接続を表すクラス。"

    def __init__(
        self, ws: WebSocketServerProtocol,
        loop: AbstractEventLoop | None = None,
        queue_size: int = 0
    ) -> None:
        self.loop = loop or get_running_loop()
        self._ws = ws

        self.queue = Queue[dict[str, Any]](queue_size)
        self.id = UUID().int

        self.fps: None | int = None
        self.interval = 0.

        # コンポーネントの用意をする。
        self.components = []
        for raw_component in avaliable_cloudable:
            c = raw_component()
            self.components.append(c)

    async def start(self) -> None:
        # FPSを受け取る。
        raw_fps = await self._ws.recv()
        assert isinstance(raw_fps, bytes)
        self.fps = int.from_bytes(raw_fps)
        self.interval = 1 / self.fps

        # 通信を始める。
        self._process_queue_task = self.loop \
            .create_task(self._process_queue())

        while True:
            await sleep(self.interval)
            for component in self.components:
                component.update()

    async def _process_queue(self) -> None:
        while True:
            await self._ws.send(dumps(await self.queue.get()))


def run() -> None:
    arun(main())


async def on_connect(websocket: WebSocketServerProtocol):
    c = Connection(websocket)
    connections[c.id] = c

    await c.start()


async def main():
    async with serve(on_connect, "localhost", 8765):
        await Future()


class CloudableCore(AbcCloudableCore):

    _is_started = False
    _connection: Connection | None = None

    def update(self, ) -> None:
        old_values = {}
        updated_values = {}

        for name in dir(self):
            value = getattr(self, name)
            if not callable(value):
                if name in old_values and old_values[name] != value:
                    updated_values[name] = value
                old_values[name] = value

        assert self._connection is not None
        self._connection.queue.put_nowait(updated_values)