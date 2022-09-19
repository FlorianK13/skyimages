import requests
from skyimages.download.constants import folsom
from skyimages.utils.config import get_project_home_dir
from tqdm import tqdm
import numpy as np
import time
from os.path import join
import os


class DownloadClass:
    def __init__(self):
        pass

    def _download_from_zenodo(self, url_dict: dict, root_dir: str) -> None:

        for filename, file_dict in url_dict.items():
            file_dir = join(root_dir, filename)
            url = file_dict["url"]
            size_tqdm = file_dict["size[Bit]"]
            data = requests.get(url, stream=True)
            import pdb

            pdb.set_trace()
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

    def _create_root_dir(self, root_dir: str) -> str:
        if root_dir is None:
            root_dir = get_project_home_dir()
        elif isinstance(root_dir, str):
            if not os.path.exists(self.root_dir):
                os.mkdir(self.root_dir)

        return root_dir


class FolsomDownloader(DownloadClass):
    def __init__(self, root_dir: str = None, data_list: list = None):
        self.data_list = data_list
        if data_list is None:
            self.data_list = folsom.DATA_LIST
        self.url_dict = folsom.DOWNLOAD_URLS
        self._confirm_download_from_user(self.url_dict)
        self.root_dir = self._create_root_dir(root_dir)

        self._download_from_zenodo(url_dict=self.url_dict, root_dir=self.root_dir)
