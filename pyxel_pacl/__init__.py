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
    if True: # もしクラウドでの実行だったら。
        run_server()
    else:
        run_client()