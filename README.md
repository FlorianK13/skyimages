# skyimages
Download sky images for solar power forecasting as pytorch-ready datasets.

## Installation
Download ``skyimages`` from
[github](https://github.com/FlorianK13/skyimages). 
Change the CWD to the download folder `skyimages/` and install
the package using pip.

```bash
git clone git@github.com:FlorianK13/skyimages.git
cd skyimages
pip install .
```


## Running code on Windows
If you use windows, wrap your code in the `if __name__ == '__main__'` clause to support multiprocessing.
[Here](https://pytorch.org/docs/stable/notes/windows.html#multiprocessing-error-without-if-clause-protection) you can find more info on this issue.
