#!/usr/bin/env python
from setuptools import setup, find_packages
import os
from spid import __version__

setup(name="spid",
    version=__version__,
    description="SPiD library for Python",
    license="MIT",
    author="SPiD",
    author_email="support@schibstedpayment.no",
    url="https://github.com/schibsted/sdk-python",
    packages=find_packages(exclude=['tests', 'examples']),
    keywords="spid library",
    zip_safe=True)
