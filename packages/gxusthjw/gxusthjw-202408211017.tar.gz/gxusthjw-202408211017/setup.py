#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        setup.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: gxusthjw包的setup.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/15     revise
# ----------------------------------------------------------------
# 打包命令 ========================================================
# python setup.py sdist bdist_wheel
# python setup.py clean --all
# 发布命令 ========================================================
# python -m twine upload --repository pypi dist/*
# 或
# python -m twine upload --repository testpypi dist/*
# =================================================================
# 导包 ============================================================
import datetime
from setuptools import setup, find_packages

# 定义 ============================================================
version = datetime.datetime.now().strftime("%Y%m%d%H%M")

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="gxusthjw",
    version=version,
    author="gxusthjw",
    author_email="jiweihuang@vip.163.com",
    description="the python packages of gxusthjw.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://codeup.aliyun.com/65445442ae64093fdcff3e06/SciWorks/gxusthjw-pytools",
    packages=find_packages(),
    install_requires=[
        'chardet',
        'typing_extensions',
        'openpyxl',

        'pytest',

        "numpy",
        "scipy",
        'sympy',
        "pandas",
        "matplotlib",
        "statsmodels",
        "lmfit",
        "findiff",
        "numdifftools",

        'nmrglue',
        "ampdLib",
        "pybaselines",

    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
