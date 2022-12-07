from skyimages.dataset import SKIPPDDataSet
import pytest
import pdb


@pytest.fixture
def skippd_testset():
    return SKIPPDDataSet(download=False, train=False)


# @pytest.fixture
# def skippd_trainset():
#    return SKIPPDDataSet(download=False, train=True)


def test_skippd_testset_dataset(skippd_testset):

    # data inof
    assert len(skippd_testset.data_info) == 4
    assert skippd_testset.data_info[0]["shape"] == (14003, 64, 64, 3)
    assert len(skippd_testset) == 14003

    dataset_path = skippd_testset.data_info[0]["file_path"]

    # data cache
    assert len(skippd_testset.data_cache) == 1
    assert len(skippd_testset.data_cache[dataset_path])
