__all__ = ("CloudableCore",)

from typing import TYPE_CHECKING
from abc import ABC, abstractstaticmethod, abstractmethod

if TYPE_CHECKING:
    from .common import Cloudable


class CloudableCore(ABC):
    """`.Cloudable`の根幹の処理の抽象基底クラス。
    このクラスは、`.Cloudable`の挙動を決定するためのものです。"""

    @abstractstaticmethod
    @staticmethod
    def init_subclass(cls_: type[Cloudable]) -> None:
        "`Cloudable`が継承された際に呼ばれる関数です。"

    @abstractmethod
    def update(self) -> None:
        "コンポーネントの`update`メソッドが実装される毎に実行される関数。"