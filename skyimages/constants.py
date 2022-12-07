import os
import pathlib

ROOT_DIR = os.path.join(os.path.expanduser("~"), ".skyimages")


FOLSOM_DOWNLOAD_URLS = {
    "NAM1": {
        "filename": "Folsom_NAM_lat38.579454_lon-121.260320.csv",
        "url": "https://zenodo.org/record/2826939/files/Folsom_NAM_lat38.579454_lon-121.260320.csv?download=1",
        "size[MB]": 1.6,
        "size[Bit]": 1599165,
    },
    "irradiance": {
        "filename": "Folsom_irradiance.csv",
        "url": "https://zenodo.org/record/2826939/files/Folsom_irradiance.csv?download=1",
        "size[MB]": 76.5,
        "size[Bit]": 76536976,
    },
    "weather": {
        "filename": "Folsom_weather.csv",
        "url": "https://zenodo.org/record/2826939/files/Folsom_weather.csv?download=1",
        "size[MB]": 138.8,
        "size[Bit]": 145500000,
    },
    "images2014": {
        "filename": "Folsom_sky_images_2014.tar.bz2",
        "url": "https://zenodo.org/record/2826939/files/Folsom_sky_images_2014.tar.bz2?download=1",
        "size[MB]": 14130,
        "size[Bit]": 14820000000,
    },
    "images2015": {
        "filename": "Folsom_sky_images_2015.tar.bz2",
        "url": "https://zenodo.org/record/2826939/files/Folsom_sky_images_2015.tar.bz2?download=1",
        "size[MB]": 17300,
        "size[Bit]": 18140000000,
    },
    "images2016": {
        "filename": "Folsom_sky_images_2016.tar.bz2",
        "url": "https://zenodo.org/record/2826939/files/Folsom_sky_images_2016.tar.bz2?download=1",
        "size[MB]": 19050,
        "size[Bit]": 19980000000,
    },
}

FOLSOM_DATA_LIST = ["NAM", "irradiance", "weather"]
FOLSOM_TRAIN_DATA = ["2014_res128.tar.bz2", "2015_res128.tar.bz2"]
FOLSOM_TEST_DATA = ["2016_res128.tar.bz2"]


SKIPPD_DOWNLOAD_URLS = {
    "dataset": {
        "filename": "2017_2019_images_pv_processed.hdf5",
        "url": "https://stacks.stanford.edu/file/druid:dj417rh1007/2017_2019_images_pv_processed.hdf5",
        "size[MB]": 4262,
        "size[Bit]": int(4262 * 1024 * 1024 * 8),
    },
}
SKIPPD_ROOT_DIR = pathlib.Path(os.path.join(ROOT_DIR, "skippd"))
