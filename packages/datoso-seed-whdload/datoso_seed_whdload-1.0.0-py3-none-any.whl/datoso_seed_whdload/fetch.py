"""Fetch and download DAT files."""
import os
import shutil
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from dateutil import tz

from datoso.configuration.folder_helper import Folders
from datoso_seed_whdload import __prefix__

NAME = 'WHDLoad'
WHDLOAD_URL = 'http://armaxweb.free.fr/'

class MyHTMLParser(HTMLParser):
    """HTML parser to get the DAT files."""

    dats: list | None = None
    rootpath = None

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """Handle the start tag of an HTML element, capture the zip hrefs."""
        if tag == 'a':
            taga = dict(attrs)
            if 'href' in taga:
                href = taga['href']
                if href.endswith('.zip') and href.startswith('dats/'):
                    self.dats.append(urljoin(self.rootpath, href).replace(' ', '%20'))


def download_dats(folder_helper: Folders) -> None:
    """Download DAT files."""

    def get_dat_links(name: str, url: str) -> list:
        """Get the DAT links."""
        print(f'Fetching {name} DAT files')
        if not url.startswith(('http:', 'https:')):
            msg = 'URL must start with "http:" or "https:"'
            raise ValueError(msg)
        red = urllib.request.urlopen(url) # noqa: S310
        pleasurehtml = red.read()

        parser = MyHTMLParser()
        parser.dats = []
        parser.rootpath = url
        parser.folder_helper = folder_helper
        parser.feed(str(pleasurehtml))
        return parser.dats

    def download_dat(href: str) -> None:
        filename = Path(href).name.replace('%20', ' ')
        if not href.startswith(('http:', 'https:')):
            msg = 'URL must start with "http:" or "https:"'
            raise ValueError(msg)
        tmp_filename, _ = urllib.request.urlretrieve(href) # noqa: S310
        local_filename = folder_helper.dats / filename
        shutil.move(tmp_filename, local_filename)

    links = get_dat_links(NAME, WHDLOAD_URL)

    print(f'Downloading {NAME} DAT files')
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(download_dat, href) for href in links
        ]
        for future in futures:
            future.result()

    path = folder_helper.dats
    files = os.listdir(folder_helper.dats)

    for file_zip in files:
        file = path / file_zip
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(path)
        Path.unlink(file)

    print('\nZipping files for backup')
    backup_daily_name = f'whdload-{datetime.now(tz.tzlocal()).strftime("%Y-%m-%d")}.zip'
    with zipfile.ZipFile(folder_helper.backup / backup_daily_name, 'w') as zip_ref:
        for root, _, files in os.walk(folder_helper.dats):
            for file in files:
                zip_ref.write(Path(root) / file, arcname=Path(root).relative_to(folder_helper.dats) / file,
                              compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def fetch() -> None:
    """Fetch and download DAT files."""
    folder_helper = Folders(seed=__prefix__)
    folder_helper.clean_dats()
    folder_helper.create_all()
    download_dats(folder_helper)
