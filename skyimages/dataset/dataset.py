from torchvision.datasets import VisionDataset
from skyimages.download.download import FolsomDownloader, SKIPPDDownloader
from skyimages.utils import create_directories, files_already_downloaded
import os
import pathlib
import pandas as pd
import numpy as np
from PIL import Image
from torchvision.datasets.utils import check_integrity
from skyimages.constants import folsom_constants, constants, skippd_constants
from typing import Any, Tuple
import pdb


class SKIPPDDataSet(VisionDataset):
    def __init__(
        self,
        root: str = None,
        train: bool = True,
        download: bool = False,
        stepsize: int = 1,
        past_steps: int = 5,
        future_steps: int = 5,
    ):
        if root is None:
            root = os.path.join(constants.ROOT_DIR)
        super().__init__(root)
        self.train = train
        self.download = download
        self._base_folder = pathlib.Path(self.root) / "skippd"
        self._images_folder = self._base_folder / "images"
        self._anns_folder = self._base_folder / "annotations"
        self._raw_folder = self._base_folder / "raw"

        self._download_urls = skippd_constants.DOWNLOAD_URLS

        create_directories([self._images_folder, self._anns_folder, self._raw_folder])

        if (
            not files_already_downloaded(
                raw_path=self._raw_folder,
                file_path_list=os.path.join(
                    self._raw_folder, self._download_urls["dataset"]["filename"]
                ),
            )
            and self.download
        ):
            downloader = SKIPPDDownloader(
                base_folder=self._raw_folder, target_folder=self._images_folder
            )
            downloader.download_and_extract()


class FolsomDataSet(VisionDataset):
    def __init__(
        self,
        root: str = None,
        train: bool = True,
        download: bool = False,
        stepsize: int = 1,
        past_steps: int = 5,
        future_steps: int = 5,
        target: str = "ghi",
    ):
        """Loads the Folsom data set.

        Parameters
        ----------
        root : str, optional
            _description_, by default None
        train : bool, optional
            _description_, by default True
        download : bool, optional
            _description_, by default False
        stepsize : int, optional
            _description_, by default 1
        past_steps : int, optional
            _description_, by default 5
        future_steps : int, optional
            _description_, by default 5

        Raises
        ------
        RuntimeError
            _description_
        """
        if root is None:
            root = os.path.join(constants.ROOT_DIR)
        super().__init__(root)
        self.train = train
        self.download = download
        self.target = target
        self._base_folder = pathlib.Path(self.root) / "folsom"
        self._images_folder = self._base_folder / "images"
        self._anns_folder = self._base_folder / "annotations"
        self._raw_folder = self._base_folder / "raw"

        if self.train:
            self._files = folsom_constants.TRAIN_DATA
        else:
            self._files = folsom_constants.TEST_DATA

        create_directories([self._images_folder, self._anns_folder, self._raw_folder])

        if not files_already_downloaded() and self.download:
            downloader = FolsomDownloader(
                base_folder=self._raw_folder, target_folder=self._images_folder
            )
            # downloader.download_and_extract(data_list=self._files)

        if not self._check_integrity():
            raise RuntimeError(
                "Dataset not found or corrupted. You can use download=True to download it"
            )

        self._data, self._annotations = self._create_data_set(
            stepsize, past_steps, future_steps
        )

    def __len__(self) -> int:
        return len(self._images)

    def __getitem__(self, index) -> Tuple[Any, Any]:
        pass

    def _create_data_set(self, stepsize, past_steps, future_steps):
        images_list = []
        for path, _, files in os.walk(self._images_folder):
            images_list.extend(os.path.join(path, name) for name in files)
        annotations_df = pd.read_csv(self._anns_folder / "Folsom_irradiance_edited.csv")
        for _, row in annotations_df:
            if row["image"] is np.nan:
                continue
            pdb.set_trace()
        return None
