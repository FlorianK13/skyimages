# skyimages
Download sky images for solar power forecasting as pytorch-ready datasets.


## Installation using pypi
From release v0.0.1, `skyimages` will be installable via pip:

```bash
pip install skyimages
```

## Installation using github
Download ``skyimages`` from
[github](https://github.com/FlorianK13/skyimages). 
Change the CWD to the download folder `skyimages/` and install
the package using pip.

```bash
git clone git@github.com:FlorianK13/skyimages.git
cd skyimages
pip install .
```

## Getting started
To download the dataset SKIPP'D ([source](https://arxiv.org/abs/2207.00913)) and use it as a pytorch torchvision dataset,
run the following code in python

```python
from skyimages.dataset.dataset import SKIPPDDataSet


traindata = SKIPPDDataSet(download=True)
testdata = SKIPPDDataSet(download=True, train=False)

trainloader = torch.utils.data.DataLoader(
    traindata, batch_size=200, shuffle=True, num_workers=0
)
testloader = torch.utils.data.DataLoader(
    testdata, batch_size=20, shuffle=False, num_workers=0
)
```

## Running code on Windows
If you use windows, wrap your code in the `if __name__ == '__main__'` clause to support multiprocessing.
[Here](https://pytorch.org/docs/stable/notes/windows.html#multiprocessing-error-without-if-clause-protection) you can find more info on this issue.
