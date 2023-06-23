from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Callable
from abc import ABC, abstractmethod, abstractstaticmethod

from .server import Connection

if TYPE_CHECKING:
    from .common import CloudableCore as AbcCloudableCore


def is_client() -> bool:
    """クライアント側で実行されているかどうかを返します。
    具体的に言うと、WebAssemblyによる実行かどうかを返します。"""
    return True


if is_client():
    from .client import CloudableCore as CloudableCore
else:
    from .server import CloudableCore as CloudableCore


class Cloudable(ABC):
    """コンポーネントを部分クラウド化することができるようにするクラス。継承して使います。
    実際にクラウド上で実行されるのは現状`.update`メソッドのみです。
    もしクライアント側で使われた場合は、このクラスは何もしません。"""

    _cloudable_original: Callable

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._cloudable_original = cls.update
        cls.update = cls._update_override
        CloudableCore.init_subclass(cls)

    @property
    def _core(self) -> AbcCloudableCore:
        if not hasattr(self, "_real_core"):
            self._real_core = CloudableCore()
        return self._real_core

    @abstractmethod
    def update(self) -> None: ...

    def _update_override(self):
        self._cloudable_original(self)
        self.core.update()