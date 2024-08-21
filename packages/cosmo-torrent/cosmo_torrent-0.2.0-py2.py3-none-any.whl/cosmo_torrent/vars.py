import os

COSMO_TORRENT_SSH_SERVER = os.environ.get(
    "COSMO_TORRENT_SSH_SERVER", "login.phys.ethz.ch"
)
COSMO_TORRENT_SSH_PORT = os.environ.get("COSMO_TORRENT_SSH_PORT", "22")

COSMO_TORRENT_REMOTE_FOLDER = os.environ.get(
    "COSMO_TORRENT_REMOTE_FOLDER",
    "/net/ipa-gate.phys.ethz.ch/export/ipa/public_html/cosmo-torrent",
)

COSMO_TORRENT_BASE_URL = os.environ.get(
    "COSMO_TORRENT_BASE_URL", "https://share.phys.ethz.ch/~ipa/cosmo-torrent"
)

MARKER_FILE = ".valid"
