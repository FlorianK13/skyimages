from skyimages.dataset import SKIPPDDataSet
import pytest
import torchvision.transforms as transforms
import torch
import pdb


@pytest.fixture
def skippd_testset():
    return SKIPPDDataSet(download=False, train=False)

@pytest.fixture
def skippd_transformed_testset():
    transform = transforms.ToTensor()
    return SKIPPDDataSet(download=False, train=False, transform=transform)



def test_skippd_testset_dataset(skippd_testset):

    # data ino
    assert len(skippd_testset.data_info) == 4
    assert skippd_testset.data_info[0]["shape"] == (14003, 64, 64, 3)
    
    # data length
    assert len(skippd_testset) == 14003

    dataset_path = skippd_testset.data_info[0]["file_path"]

    # data cache
    assert len(skippd_testset.data_cache) == 1
    assert len(skippd_testset.data_cache[dataset_path])
    
    # data get item
    assert skippd_testset[0][0].shape==torch.Size([64, 64, 3])
    

def test_skippd_testset_dataloader(skippd_transformed_testset):
    batch_size = 5
    dataloader = torch.utils.data.DataLoader(skippd_transformed_testset, batch_size=batch_size, shuffle=False, num_workers=0)
    batch = next(iter(dataloader))
    
    assert len(batch) == 2
    assert len(batch[0]) == batch_size
    