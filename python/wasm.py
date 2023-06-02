
from functools import cached_property
from dataclasses import dataclass

from sys import platform

from .types_ import Cloudable as AbcCloudable


@dataclass
class CloudDetails:
    "クラウド側の接続先の情報を格納するのに使うデータクラスです。"

    host: str
    port: int


class Cloudable(AbcCloudable):
    "WebAssemblyだった際にクラウド化する、部分的クラウド化を支援するためのクラスです。"

    @cached_property
    def use_cloud(self) -> bool:
        return platform in ("emscripten", "wasi")

    def connect(self) -> None:
        if not self.use_cloud:
            return

        ...