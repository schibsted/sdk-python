#!/usr/bin/env python
from setuptools import setup, find_packages
import os
from spid import __version__

long_description = ""
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

setup(name="spid",
    version=__version__,
    description="SPiD library for Python",
    long_description=long_description,
    license="MIT",
    author="SPiD",
    author_email="support@schibstedpayment.no",
    url="https://github.com/schibsted/sdk-python",
    packages=find_packages(exclude=['tests', 'examples']),
    keywords="spid library",
    zip_safe=True)
