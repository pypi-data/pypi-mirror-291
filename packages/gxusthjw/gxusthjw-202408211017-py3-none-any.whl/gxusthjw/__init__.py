#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: gxusthjw包的__init__.py。
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
# 导包 ============================================================
from . import axs
from . import baselines
from . import commons
from . import datatable
from . import experiment
from . import findpeaks
from . import fittings
from . import fitykers
from . import fityks
from . import fsd
from . import ftir
from . import genetic
from . import ma
from . import mathematics
from . import matlabs
from . import nmr
from . import origins
from . import partitions
from . import peakfits
from . import raman
from . import spectrum
from . import statistics
from . import ta
from . import units
from . import xps
from . import xrd
from . import zhxyao

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
the python packages of gxusthjw.
"""

__all__ = [
    'axs',
    'baselines',
    'commons',
    'datatable',
    'experiment',
    'findpeaks',
    'fittings',
    'fitykers',
    'fityks',
    'fsd',
    'ftir',
    'genetic',
    'ma',
    'mathematics',
    'matlabs',
    'nmr',
    'origins',
    'partitions',
    'peakfits',
    'raman',
    'spectrum',
    'statistics',
    'ta',
    'units',
    'xps',
    'xrd',
    'zhxyao',
]
# ==================================================================
