from setuptools import find_packages
from setuptools import setup

setup(
    name='nav2_common',
    version='1.3.6',
    packages=find_packages(
        include=('nav2_common', 'nav2_common.*')),
)
