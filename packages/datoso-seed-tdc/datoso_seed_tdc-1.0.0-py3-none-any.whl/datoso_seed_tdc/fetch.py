"""Fetch and download DAT files."""
import zipfile
from datetime import datetime
from pathlib import Path

from dateutil import tz

from datoso.configuration.folder_helper import Folders
from datoso.helpers import FileUtils, show_progress
from datoso.helpers.download import downloader
from datoso_seed_tdc import __prefix__


def download_dats(folder_helper: Folders) -> None:
    """Download DAT files."""
    href = 'http://www.totaldoscollection.org/nugnugnug/tdc_daily_paths.zip'
    filename = Path(href).name
    local_filename = folder_helper.dats / filename
    print(f'Downloading {filename}')
    downloader(url=href, destination=local_filename, reporthook=show_progress)

    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(folder_helper.dats)
    backup_daily_name = f'tdc-{datetime.now(tz.tzlocal()).strftime("%Y-%m-%d")}.zip'

    FileUtils.move(local_filename, Path(folder_helper.backup)  / backup_daily_name)

def fetch() -> None:
    """Fetch and download DAT files."""
    folder_helper = Folders(seed=__prefix__)
    folder_helper.clean_dats()
    folder_helper.create_all()
    download_dats(folder_helper)
