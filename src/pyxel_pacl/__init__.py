__all__ = ("run_server", "run_client", "Cloudable", "run")

try:
    from .server import run as run_server
except ModuleNotFoundError:
    run_server = lambda: None
try:
    from .client import run as run_client
except ModuleNotFoundError:
    run_client = lambda: None
from .common import Cloudable


def run() -> None:
    "環境によってクライアントまたはサーバーを動かします。"
    if True: # もしクラウドでの実行だったら。
        run_server()
    else:
        run_client()