# cosmo-torrent

This project offers a library to access data from central storage location
and a command line tool to upload data.

This can be used to avoid shipping large data sets within Python packages.

## Data upload

After installing `cosmo-torrent` the command line command

```
$ cosmo-torrent-upload --help
Usage: cosmo-torrent-upload [OPTIONS] FOLDER

Options:
  --identifier TEXT  data set identifier for later download  [required]
  --user TEXT        user name for scp to server
  --force            overwrite existing dataset
  --help             Show this message and exit.
```

can be used to upload data to a central storage location (details in the
[Internals](#Internals) section below).

For example:

```
$ cosmo-torrent-upload --identifier test_data.2024.08 --user schmittu .
```
uploads the content of the current working folder using the identifier
`test_data.2024.08`.

## Data accesss

The data can be accessed using the identifier used for the upload.
On first access, the data is downloaded to a local cache folder.
For future access, the dataset can be accessed directly.


```python
from cosmo_torrent import data_set

test_data_folder = data_set('test_data.2024.07')
```

Here `test_data_folder` will now be a local folder with the specified data set.



## Internals

The data is stored at
`/net/ipa-gate.phys.ethz.ch/export/ipa/public_html/cosmo-torrent` at the DPHYS NAS
which can be accessed via https://share.phys.ethz.ch/~ipa/cosmo-torrent
