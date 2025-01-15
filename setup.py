# File: setup.py

from setuptools import setup, find_packages

setup(
    name="prototype",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.3',
        'pandas==1.5.3',
        'pyyaml==5.4.1',
    ],
)