import os


def create_directories(directory_list: list) -> None:
    """Check if directories already exist, create them if not.
    Parameters
    ----------
    directory_list : list
        list of directory paths.
    """
    for path in directory_list:
        if not os.path.exists(path):
            os.makedirs(path)


def files_already_downloaded(raw_path: str, file_list: list) -> bool:
    """Checks if the files from the given list are in
    the given path (and subdirectories)

    Parameters
    ----------
    raw_path : str
        Path to a directory
    file_list : list
        Files that might be in the given path

    Returns
    -------
    bool
        True if all files are in the directory
    """
    all_files = []
    for _, _, files in os.walk(raw_path):
        all_files += files
    for file in file_list:
        if file not in all_files:
            return False

    return True
