from skyimages.utils import create_directories, files_already_downloaded
import os
from os.path import expanduser, join


def test_create_directories():
    directory_path = join(expanduser("~"), ".testdirectory")
    directory_list = [directory_path]
    create_directories(directory_list=directory_list)
    assert os.path.exists(directory_path)
    os.rmdir(directory_path)
