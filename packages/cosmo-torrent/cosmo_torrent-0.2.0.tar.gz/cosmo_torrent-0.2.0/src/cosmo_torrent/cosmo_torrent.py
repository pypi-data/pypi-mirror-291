# Copyright (C) 2024 ETH Zurich, Institute for Particle Physics and Astrophysics

import hashlib
import os
import sys
import tempfile
import zipfile

import requests
import tqdm
from requests.exceptions import HTTPError

from .vars import COSMO_TORRENT_BASE_URL, MARKER_FILE


def data_path(identifier):
    cache_folder = local_cache_folder(identifier)
    if not is_valid(cache_folder):
        download_data(identifier, cache_folder)
    return cache_folder


def _md5_sum(path, CHUNK_SIZE=512 * 1024**2):
    digest = hashlib.md5()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(CHUNK_SIZE)
            if not chunk:
                return digest.hexdigest()
            digest.update(chunk)


def local_cache_folder(identifier):
    return os.path.join(_cache_base_folder(), identifier)


def _cache_base_folder():
    home = os.path.expanduser("~")
    if sys.platform.startswith("darwin"):
        base_folder = os.path.join(home, "Library", "Cache", "cosmo-torrent")
    else:
        base_folder = os.path.join(home, "_cache", "cosmo-torrent")
    return base_folder


def is_valid(cache_folder):
    return os.path.exists(os.path.join(cache_folder, MARKER_FILE))


def download_data(
    identifier, cache_folder, COSMO_TORRENT_BASE_URL=COSMO_TORRENT_BASE_URL
):
    _download_and_check_data(identifier, cache_folder, COSMO_TORRENT_BASE_URL)
    with open(os.path.join(cache_folder, MARKER_FILE), "w"):
        pass


def download(url, target, show_progressbar):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024 * 1024
        with tqdm.tqdm(
            total=total_size,
            unit_scale=True,
            unit="B",
            unit_divisor=block_size,
            disable=not show_progressbar,
        ) as progress_bar:
            with open(target, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise IOError("data set does not exist")
        raise e


def _download_and_check_data(identifier, cache_folder, url):
    with tempfile.TemporaryDirectory() as download_folder:
        archive = identifier + ".zip"
        downloaded_archive = os.path.join(download_folder, archive)
        download(url.rstrip("/") + "/" + archive, downloaded_archive, True)

        md5 = identifier + ".md5"
        downloaded_md5 = os.path.join(download_folder, md5)
        download(url.rstrip("/") + "/" + md5, downloaded_md5, False)

        if check_downloaded_data(downloaded_archive, downloaded_md5):
            with zipfile.ZipFile(downloaded_archive, "r") as zh:
                zh.extractall(cache_folder)
            return cache_folder
    raise IOError("checksum failure after download")


def check_downloaded_data(downloaded_archive, downloaded_md5):
    with open(downloaded_md5, "r") as fh:
        md5sum = fh.read().strip()

    return _md5_sum(downloaded_archive) == md5sum


if __name__ == "__main__":
    print(data_path("ucat.test"))
