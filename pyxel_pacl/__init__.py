
from .server import run as run_server


def run() -> None:
    if True: # もしクラウドでの実行だったら。
        run_server()