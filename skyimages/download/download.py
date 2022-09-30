import requests
from skyimages.constants import folsom_constants
from tqdm import tqdm
import numpy as np
import time
import os
from os.path import join
import tarfile
import pdb


class DownloadClass:
    def __init__(self):
        pass

    def _download_from_zenodo(self, url_dict: dict, root_dir: str) -> None:

        for filename, file_dict in url_dict.items():
            file_dir = join(root_dir, filename)
            url = file_dict["url"]
            size_tqdm = file_dict["size[Bit]"]
            data = requests.get(url, stream=True)
            time_a = time.perf_counter()
            with open(file_dir, "wb") as zfile, tqdm(file_dir, total=size_tqdm) as bar:
                for chunk in data.iter_content():
                    if chunk:
                        zfile.write(chunk)
                        zfile.flush()
                    bar.update(len(chunk))
            time_b = time.perf_counter()
            print(
                f"Download of {filename} is finished. It took {int(np.around(time_b - time_a))} seconds."
            )

    def _confirm_download_from_user(self, url_dict: dict) -> None:
        pass

    def _extract_tar_bz2(self, path, target) -> None:
        with tarfile.open(path, "r:bz2") as tar:
            tar.extractall(path=target)
            pdb.set_trace()


class FolsomDownloader(DownloadClass):
    def __init__(self, base_folder: str, target_folder: str, files: list = None):
        self.files = files
        self.url_dict = folsom_constants.DOWNLOAD_URLS
        self._base_folder = base_folder
        self._target_folder = target_folder

    def download_and_extract(self, data_list: list) -> None:
        self._confirm_download_from_user(self.url_dict)
        # self._download_from_zenodo(url_dict=self.url_dict, root_dir=self.root_dir)
        for data in data_list:
            self._extract_tar_bz2(
                path=self._base_folder / data, target=self._target_folder
            )
