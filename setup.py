from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="skyimages",
    packages=[
        "skyimages",
        "skyimages.dataset",
        "skyimages.download",
    ],
    version="0.0.1",
    description="Downloading sky images for ML applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Florian Kotthoff",
    author_email="kotthoff@fortiss.org",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6, <4",
    install_requires=["torch", "requests", "tqdm"],
    extras_require={"dev": []},
)
