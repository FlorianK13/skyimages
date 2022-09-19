from torch.utils.data import Dataset
from skyimages.download.download import FolsomDownloader


class FolsomDataSet(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        downloader = FolsomDownloader(root_dir=self.root_dir)

    def __len__(self):
        pass

    def __getitem__(self, index):
        pass
