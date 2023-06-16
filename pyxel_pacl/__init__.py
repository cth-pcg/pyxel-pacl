
from .server import prepare as prepare_server


def prepare() -> None:
    if True: # もしクラウドでの実行だったら。
        prepare_server()