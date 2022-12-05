from torchvision.datasets import VisionDataset
from skyimages import constants
from skyimages.download import FolsomDownloader, SKIPPDDownloader
from skyimages.utils import create_directories, files_already_downloaded
import os
import pathlib
import pandas as pd
import numpy as np
from PIL import Image
from torchvision.datasets.utils import check_integrity
from skyimages import constants
from typing import Any, Tuple
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

        self._download_urls = constants.SKIPPD_DOWNLOAD_URLS

        ### From hdf5
        self.data_info = []
        # List of dictionaries, each dictionary contains info of one dataset of a specific hdf5 file
        self.data_cache = {}
        # Dictionary: Keys are the filepaths of the hdf5 files, value is a list of the dataset within the hdf5 file
        self.data_cache_size = data_cache_size
        self.transform = transform

        if self.train:
            self.hdf5_images_key = "/trainval/images_log"
            self.hdf5_annotations_key = "/trainval/pv_log"
        else:
            self.hdf5_images_key = "/test/images_log"
            self.hdf5_annotations_key = "/test/pv_log"
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

        if not self._check_integrity():
            raise RuntimeError(
                "Dataset not found or corrupted. You can use download=True to download it"
            )

        for h5dataset_fp in os.listdir(self._raw_folder):
            self._fill_data_info_list_and_load_to_cache(
                os.path.join(self._raw_folder, h5dataset_fp), load_data
            )
        # self.data_info =
        # [{'file_path': 'C:\\Users\\kotthoff\\.skyimages\\skippd\\raw\\2017_2019_images_pv_processed.hdf5', 'name': '/test/images_log', 'category': '/test', 'shape': (14003, 64, 64, 3), 'cache_idx': 0}
        # {'file_path': 'C:\\Users\\kotthoff\\.skyimages\\skippd\\raw\\2017_2019_images_pv_processed.hdf5', 'name': '/test/pv_log', 'category': '/test', 'shape': (14003,), 'cache_idx': 1}
        # {'file_path': 'C:\\Users\\kotthoff\\.skyimages\\skippd\\raw\\2017_2019_images_pv_processed.hdf5', 'name': '/trainval/images_log', 'category': '/trainval', 'shape': (349372, 64, 64, 3), 'cache_idx': 2}
        # {'file_path': 'C:\\Users\\kotthoff\\.skyimages\\skippd\\raw\\2017_2019_images_pv_processed.hdf5', 'name': '/trainval/pv_log', 'category': '/trainval', 'shape': (349372,), 'cache_idx': 3}]

        self.length = self.get_data_infos(self.hdf5_annotations_key)["shape"][0]

    def __getitem__(self, index):
        # get data
        x = self.get_dataset(self.hdf5_images_key)[index]
        x = self.transform(x) if self.transform else torch.from_numpy(x)

        # get label
        y = self.get_dataset(self.hdf5_annotations_key)[index]
        y = torch.from_numpy(y) if type(y) == np.array else torch.tensor([y])
        return (x, y)

    def __len__(self):
        return self.length

    def _fill_data_info_list_and_load_to_cache(
        self, file_path: pathlib.Path, load_data: bool
    ):
        """Fills the self.data_info list with basic info.

        Parameters
        ----------
        file_path : pathlib.Path
            Path of the folder for the raw data files
        load_data : bool
            If True, data is loaded to cache
        """
        # h5_file = h5py.File(file_path)
        with h5py.File(file_path) as h5_file:
            # Walk through all groups, extracting datasets
            for _, group in h5_file.items():
                for dname, ds in group.items():
                    # if data is not loaded its cache index is -1
                    idx = -1
                    if load_data:
                        idx = self._add_to_cache(ds[:], file_path)
                        # Use ds[:] to avoid handeling closed datasets

                    # type is derived from the name of the dataset; we expect the dataset
                    # name to have a name such as 'data' or 'label' to identify its type
                    # we also store the shape of the data in case we need it
                    self.data_info.append(
                        {
                            "file_path": file_path,
                            "name": f"{group.name}/{dname}",
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
    def get_dataset(self, dataset_caller: str):
        """Call this function anytime you want to access one of the
        dataset. This will make sure that the data is loaded in case it is
        not part of the data cache.

        Parameters
        ----------
        dataset_caller : str
            string that is used to find the dataset in the hdf5 file.
            In the format: 'folder1/folder2/.../dataset_name'

        Returns
        -------
        _type_
            _description_
        """

        dataset_metadata = self.get_data_infos(dataset_caller)

        fp = dataset_metadata["file_path"]
        if fp not in self.data_cache:
            self._load_data(fp)

        # get new cache_idx assigned by _load_data_info
        cache_idx = dataset_metadata["cache_idx"]

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
                    # Use ds[:] to avoid handling closed hdf5 datasets

                    # find the beginning index of the hdf5 file we are looking for
                    file_idx = next(
                        i
                        for i, v in enumerate(self.data_info)
                        if v["file_path"] == file_path
                    )

                    # the data info should have the same index since we loaded it in the same way
                    self.data_info[file_idx + idx]["cache_idx"] = idx

        # remove an element from data cache if size was exceeded
        # if len(self.data_cache) > self.data_cache_size:
        #     # remove one item from the cache at random
        #     removal_keys = list(self.data_cache)
        #     removal_keys.remove(file_path)
        #     self.data_cache.pop(removal_keys[0])
        #     # remove invalid cache_idx
        #     self.data_info = [
        #         {
        #             "file_path": di["file_path"],
        #             "name": di["name"],
        #             "shape": di["shape"],
        #             "cache_idx": -1,
        #         }
        #         if di["file_path"] == removal_keys[0]
        #         else di
        #         for di in self.data_info
        #     ]

    def get_data_infos(self, dataset_caller) -> list:
        """Get dataset metadata for the dataset defined by dataset_caller."""
        for dataset_metadata in self.data_info:
            if dataset_metadata["name"] == dataset_caller:
                return dataset_metadata

    def _check_integrity(self) -> bool:
        """Returns `True` if at least one file of `.hdf5` format is in the raw folder."""
        return bool(
            [file for _, _, file in os.walk(self._raw_folder) if ".hdf5" in file]
        )


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
            self._files = constants.FOLSOM_TRAIN_DATA
        else:
            self._files = constants.FOLSOM_TEST_DATA

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
        return None