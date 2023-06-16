
from collections.abc import Callable
from abc import ABC, abstractmethod

from .server import connections


class Cloudable(ABC):

    _cloudable_original: Callable

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._cloudable_original = cls.update
        cls.update = cls._update_override

    @abstractmethod
    def update(self) -> None: ...

    def _update_override(self):
        old_values = {}
        updated_values = {}
        self._cloudable_original(self)
        for name in dir(self):
            value = getattr(self, name)
            if not callable(value):
                if name in old_values and old_values[name] != value:
                    updated_values[name] = value
                old_values[name] = value
        connections[id_].queue.put(updated_values)