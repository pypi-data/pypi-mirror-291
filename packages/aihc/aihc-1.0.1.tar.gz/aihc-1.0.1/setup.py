#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Setup script.

Authors: wangzhuyun(wangzhuyun@baidu.com)
Date:    2024/08/08 10:43:35
"""
import os
from setuptools import setup, find_packages
from distutils.core import setup
with open("README.rst", "r") as file:
    long_description = file.read()
# from pkg_resources import parse_requirements
# with open("requirements.txt", encoding="utf-8") as fp:
#     install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name='aihc',
    version='1.0.1',
    description='AIHC Command-Line Tool',
    long_description=long_description,
    author='Baiduclear Corporation',
    author_email='wangzhuyun@baidu.com',
    url='https://github.com/Baidu-AIHC/aihc_cli',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'aihc_cli_py': ['doc/*.txt'],
    },
    install_requires=[
        'datetime',
        'pandas',
        'requests',
    ],
    entry_points={
        'console_scripts': ['aihc = aihc_cli_py.runner:main']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)