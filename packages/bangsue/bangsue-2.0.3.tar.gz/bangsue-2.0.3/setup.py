import setuptools
from setuptools.config import read_configuration
from pathlib import Path

conf_dict = read_configuration("setup.cfg")
with open('requirements.txt') as f:
    required = f.read().splitlines()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="bangsue",
    version="2.0.3",
    author="ARSANANDHA",
    author_email="arsanandha.ap@gmail.com",
    description="Bangsue. Thai Codename Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aphisitworachorch/bangsue",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)
