from skyimages.utils import create_directories, files_already_downloaded
import os
from os.path import join
import shutil
import tempfile


def test_create_directories():
    directory_path = join(tempfile.gettempdir(), ".testdirectory")
    directory_list = [directory_path]

    # Create directory
    create_directories(directory_list=directory_list)

    # handle existing directories
    create_directories(directory_list=directory_list)
    assert os.path.exists(directory_path)
    os.rmdir(directory_path)


def test_files_already_downloaded():
    directory_path = join(tempfile.gettempdir(), ".testdirectory")
    os.makedirs(directory_path)
    file_list = [
        "test1.txt",
        "test2.txt",
    ]

    # create files in directory
    for filepath in file_list:
        open(join(directory_path, filepath), "a").close()

    assert files_already_downloaded(raw_path=directory_path, file_list=file_list)

    file_list.append("test3.txt")

    assert not files_already_downloaded(raw_path=directory_path, file_list=file_list)

    shutil.rmtree(directory_path)
