# skyimages

[![PyPI - Downloads](https://img.shields.io/pypi/dm/skyimages?label=pypi%20downloads)](https://pypistats.org/packages/skyimages)
[![GitHub issues by-label](https://img.shields.io/github/issues-raw/FlorianK13/skyimages/good%20first%20issue?label=Contribute%3A%20Good%20first%20issue)](https://github.com/FlorianK13/skyimages/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

Download sky images for solar power forecasting as pytorch-ready datasets.
The package is still in early development and not stable. Please report bugs in the [Issues](https://github.com/FlorianK13/skyimages/issues).



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
from skyimages.dataset import SKIPPDDataSet
import torch


traindata = SKIPPDDataSet(download=True)
testdata = SKIPPDDataSet(download=True, train=False)

trainloader = torch.utils.data.DataLoader(
    traindata, batch_size=200, shuffle=True, num_workers=0
)
testloader = torch.utils.data.DataLoader(
    testdata, batch_size=20, shuffle=False, num_workers=0
)
```

## Implemented data sets
* [SKIPPD](https://arxiv.org/abs/2207.00913)

## Contributing
Contributions and cooperations are highly welcome. If interested, just create an issue and we can discuss further details.
