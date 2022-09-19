import os


def get_project_home_dir():
    """Get root dir of project data
    On linux this path equals `$HOME/.skyimages/`, respectively `~/.skyimages/`

    Returns
    -------
    path-like object
        Absolute path to root dir of open-MaStR project home
    """

    return os.path.join(os.path.expanduser("~"), ".skyimages")
