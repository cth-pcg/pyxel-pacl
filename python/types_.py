
from typing import Any
from abc import ABC, abstractmethod


class Cloudable(ABC):
    @property
    @abstractmethod
    def use_cloud(self) -> bool:
        "クラウド側との連携を必要とするかどうかです。"

    @abstractmethod
    def connect(self) -> None:
        "接続を行います。`.use_cloud`が`False`を返す場合、これは何もしません。"