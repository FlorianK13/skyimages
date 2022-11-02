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
import h5py
import torch


# some of the code comes from: https://gist.github.com/branislav1991/4c143394bdad612883d148e0617bdccd


class SKIPPDDataSet(VisionDataset):
    def __init__(
        self,
        root: str = None,
        train: bool = True,
        download: bool = False,
        stepsize: int = 1,
        past_steps: int = 5,
        future_steps: int = 5,
        data_cache_size: int = 3,
        load_data: bool = True,
        transform=None,
    ):
        """Pytorch dataset for the SKIPPD sky images.

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
        data_cache_size : int, optional
            _description_, by default 3
        load_data : bool, optional
            Determines if the data is loaded to cache, by default True
        transform : _type_, optional
            _description_, by default None
        """
        if root is None:
            root = os.path.join(constants.ROOT_DIR)
        super().__init__(root)

        ### Define Attributes
        self.train = train
        self.download = download
        self._base_folder = pathlib.Path(self.root) / "skippd"
        self._images_folder = self._base_folder / "images"
        self._anns_folder = self._base_folder / "annotations"
        self._raw_folder = self._base_folder / "raw"

        self._download_urls = skippd_constants.DOWNLOAD_URLS

        ### From hdf5
        self.data_info = []
        self.data_cache = {}
        self.data_cache_size = data_cache_size
        self.transform = transform

        if self.train:
            self.hdf5_images_key = "trainval", "images_log"
            self.hdf5_annotations_key = "trainval", "pv_log"
        else:
            self.hdf5_images_key = "test", "images_log"
            self.hdf5_annotations_key = "test", "pv_log"
        ### END Define Attributes

        create_directories([self._images_folder, self._anns_folder, self._raw_folder])

        if (
            not files_already_downloaded(
                raw_path=self._raw_folder,
                file_path_list=[self._download_urls["dataset"]["filename"]],
            )
            and self.download
        ):
            downloader = SKIPPDDownloader(
                base_folder=self._raw_folder, target_folder=self._images_folder
            )
            downloader.download_and_extract()

        for h5dataset_fp in os.listdir(self._raw_folder):
            self._add_data_infos(
                os.path.join(self._raw_folder, h5dataset_fp), load_data
            )

    def __getitem__(self, index):
        # get data
        category = "/trainval" if self.train else "/test"
        x = self.get_data(self.hdf5_images_key, category, index)
        x = self.transform(x) if self.transform else torch.from_numpy(x)

        # get label
        y = self.get_data(self.hdf5_annotations_key, index)
        y = torch.from_numpy(y)
        return (x, y)

    def __len__(self):
        return len(self.get_data_infos(self.hdf5_images_key))

    def _add_data_infos(self, file_path, load_data):
        # h5_file = h5py.File(file_path)
        with h5py.File(file_path) as h5_file:

            # Walk through all groups, extracting datasets
            for _, group in h5_file.items():
                for dname, ds in group.items():
                    # if data is not loaded its cache index is -1
                    idx = -1
                    if load_data:
                        # add data to the data cache
                        idx = self._add_to_cache(ds[:], file_path)

                    # type is derived from the name of the dataset; we expect the dataset
                    # name to have a name such as 'data' or 'label' to identify its type
                    # we also store the shape of the data in case we need it
                    self.data_info.append(
                        {
                            "file_path": file_path,
                            "type": dname,
                            "category": group.name,
                            "shape": ds.shape,
                            "cache_idx": idx,
                        }
                    )

    def _add_to_cache(self, data, file_path):
        """Adds data to the cache and returns its index. There is one cache
        list for every file_path, containing all datasets in that file.
        """
        if file_path not in self.data_cache:
            self.data_cache[file_path] = [data]
        else:
            self.data_cache[file_path].append(data)
        return len(self.data_cache[file_path]) - 1

    ### __getitem__ helper functions start from here
    def get_data(self, type, category, i):
        """Call this function anytime you want to access a chunk of data from the
        dataset. This will make sure that the data is loaded in case it is
        not part of the data cache.
        """
        fp = self.get_data_infos(type)[i]["file_path"]
        if fp not in self.data_cache:
            pdb.set_trace()
            self._load_data(fp)

        # get new cache_idx assigned by _load_data_info
        cache_idx = self.get_data_infos(type)[i]["cache_idx"]
        return self.data_cache[fp][cache_idx]

    def _load_data(self, file_path):
        """Load data to the cache given the file
        path and update the cache index in the
        data_info structure.
        """
        with h5py.File(file_path) as h5_file:
            for _, group in h5_file.items():
                for _, ds in group.items():
                    # add data to the data cache and retrieve
                    # the cache index
                    idx = self._add_to_cache(ds[:], file_path)

                    # find the beginning index of the hdf5 file we are looking for
                    file_idx = next(
                        i
                        for i, v in enumerate(self.data_info)
                        if v["file_path"] == file_path
                    )

                    # the data info should have the same index since we loaded it in the same way
                    self.data_info[file_idx + idx]["cache_idx"] = idx

        # remove an element from data cache if size was exceeded
        if len(self.data_cache) > self.data_cache_size:
            # remove one item from the cache at random
            removal_keys = list(self.data_cache)
            removal_keys.remove(file_path)
            self.data_cache.pop(removal_keys[0])
            # remove invalid cache_idx
            self.data_info = [
                {
                    "file_path": di["file_path"],
                    "type": di["type"],
                    "shape": di["shape"],
                    "cache_idx": -1,
                }
                if di["file_path"] == removal_keys[0]
                else di
                for di in self.data_info
            ]

    def get_data_infos(self, type):
        """Get data infos belonging to a certain type of data."""
        return [di for di in self.data_info if di["type"] in type]


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
