"""Setup for pysmarty2 package."""

import setuptools


with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="pysmarty2",
    version="0.10.1",
    author="Martins Sipenko, Theo Nicolaum",
    author_email="martins.sipenko@gmail.com",
    description="Python API for Salda Smarty Modbus TCP",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/martinssipenko/pysmarty2",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
