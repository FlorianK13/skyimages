from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="skyimages",
    version="0.0.2a1",
    description="Downloading sky image datasets for pytorch applications",
    author="Florian Kotthoff",
    author_email="flo.pypi@posteo.de",
    url="https://github.com/FlorianK13/skyimages",
    packages=[
        "skyimages",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.6, <4",
    install_requires=["torch", "torchvision", "requests", "tqdm", "h5py", "pandas"],
    extras_require={"dev": []},
)
