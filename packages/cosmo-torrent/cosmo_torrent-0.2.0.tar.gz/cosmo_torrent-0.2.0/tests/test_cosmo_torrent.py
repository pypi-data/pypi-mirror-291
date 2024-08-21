import os
import socket
import threading
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import urlretrieve

from cosmo_torrent.cli import _list, _upload
from cosmo_torrent.cosmo_torrent import download_data


def _free_port():
    # https://stackoverflow.com/questions/1365265
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def test_upload_and_download(tmpdir_factory, regtest):
    user = os.environ.get("USER")
    data_to_upload_folder = tmpdir_factory.mktemp("data")
    data_to_upload_folder.join("data.txt").write_text("abc", "utf-8")

    local_data_storage = tmpdir_factory.mktemp("storage").strpath

    assert (
        _upload(
            "test",
            user,
            data_to_upload_folder,
            False,
            "localhost",
            22,
            local_data_storage,
        )
        == 0
    )

    p = _free_port()

    try:
        server = HTTPServer(
            ("", p), partial(SimpleHTTPRequestHandler, directory=local_data_storage)
        )
        t = threading.Thread(target=server.serve_forever)
        t.start()

        url = f"http://localhost:{p}"
        assert _list(url) == ["test"]

        downloaded, _ = urlretrieve(url)
        print(open(downloaded).read(), file=regtest)

        download_folder = tmpdir_factory.mktemp("downloads")

        download_data("test", download_folder.strpath, url)
        for p in download_folder.listdir():
            print(p.strpath, file=regtest)

    finally:
        server.shutdown()
        t.join()
