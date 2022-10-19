import os
import pdb


def create_directories(directory_list):
    """Check if directories already exist, create them if not.
    Parameters
    ----------
    directory_list : list
        list of directory paths.
    """
    for path in directory_list:
        if not os.path.exists(path):
            os.makedirs(path)


def files_already_downloaded(raw_path: str, file_path_list: list) -> bool:
    all_files = []
    for _, _, files in os.walk(raw_path):
        all_files += files
    for file in file_path_list:
        if file not in all_files:
            return False
    return True
