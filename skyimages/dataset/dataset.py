from torch.utils.data import Dataset
from skyimages.download import FolcomDownloader


class FolsomDataSet(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        downloader = FolcomDownloader()
    
    def __len__(self):
        pass
    
    def __getitem__(self, index):
        pass
