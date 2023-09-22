from .types_ import CloudableCore as AbcCloudableCore

def run() -> None:
    ...

class CloudableCore(AbcCloudableCore):
    def update(self) -> None:
        "Pyxelのコンポーネントの`update`が呼ばれることを期待する。"