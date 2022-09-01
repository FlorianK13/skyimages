from skyimages.utils.path import file_exists

def DownloadClass():
    def __init__(self):
        pass
    
    def _download_from_zenodo(url_dict:dict):
        pass


def FolcomDownloader(DownloadClass):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.url_dict = {}
        if not file_exists(self.root_dir):
            self._download_from_zenodo(self.url_dict)
            
    