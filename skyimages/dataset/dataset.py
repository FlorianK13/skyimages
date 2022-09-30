from torchvision.datasets import VisionDataset
from skyimages.download.download import FolsomDownloader
import os
import pathlib
import pandas as pd
from PIL import Image
from torchvision.datasets.utils import check_integrity
from skyimages.constants import folsom_constants, constants
from typing import Any, Tuple
import pdb


class FolsomDataSet(VisionDataset):
    def __init__(self, root: str = None, train: bool = True, download: bool = False):
        if root is None:
            root = os.path.join(constants.ROOT_DIR)
        super().__init__(root)
        self.train = train
        self.download = download
        self._base_folder = pathlib.Path(self.root) / "folsom"
        self._images_folder = self._base_folder / "images"
        self._anns_folder = self._base_folder / "annotations"

        if self.train:
            self._files = folsom_constants.TRAIN_DATA
        else:
            self._files = folsom_constants.TEST_DATA

        for path in [self._images_folder, self._anns_folder]:
            if not os.path.exists(path):
                os.makedirs(path)

        if not self._files_already_downloaded() and self.download:
            downloader = FolsomDownloader(
                base_folder=self._base_folder, target_folder=self._images_folder
            )
            # downloader.download_and_extract(data_list=self._files)

        if not self._check_integrity():
            raise RuntimeError(
                "Dataset not found or corrupted. You can use download=True to download it"
            )
        self._images = []
        for path, _, files in os.walk(root):
            self._images.extend(os.path.join(path, name) for name in files)
        self._annotations = pd.read_csv(self._anns_folder / "Folsom_irradiance.csv")
        pdb.set_trace()

    def __len__(self) -> int:
        return len(self._images)

    def __getitem__(self, index) -> Tuple[Any, Any]:
        image = Image.open(self._images[index]).convert("RGB")
        return image

    def _check_integrity(self) -> bool:
        return True
        """root = self.root
        for fentry in self.train_list + self.test_list:
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True"""

    def _files_already_downloaded(self) -> bool:
        for zipped_folder in self._files:
            folder = zipped_folder.split(".")[0]
            if not os.path.exists(self.root + folder):
                return False
        return True
