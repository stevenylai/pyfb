#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from tornado_pyfb import __author__, __version__, __license__

setup(
    name='tornado_pyfb',
    version=__version__,
    description='A Python Interface to the Facebook Graph API',
    author=__author__,
    author_email="jmg.utn@gmail.com",
    license=__license__,
    keywords="Facebook Graph API Wrapper Python",
    url='https://github.com/stevenylai/tornado_pyfb',
    packages=['tornado_pyfb'],
)
