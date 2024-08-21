#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: gxusthjw.commons包的__init__.py。
#                                  承载“常见的”函数和类。
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
from .array_utils import (is_sorted,
                          is_sorted_ascending,
                          is_sorted_descending,
                          reverse,
                          Ordering,
                          is_equals_of,
                          sort)
from .data_capsule import DataCapsule

from .exceptions import ExceptionBase,StateException
from .file_object import (get_file_encoding_chardet,
                          file_info,
                          get_file_info,
                          get_file_info_of_module,
                          get_file_object,
                          FileInfo,
                          FileObject)

from .file_reader import read_txt
from .gxusthjw_base import (Base, Author, Version, Copyright)
from .math_plus import traditional_round
from .monotonic_functions import (monotonic_power,
                                  monotonic_linear,
                                  monotonic_log)
from .numerical_constant import (NUMERICAL_PRECISION,
                                 float_epsilon, ARITHMETIC_PRECISION,
                                 TINY_FLOAT, FLOAT_EPSILON,
                                 BOLTZMANN_CONSTANT, GAS_CONSTANT,
                                 AVOGADRO_CONSTANT)
from .numpy_plus import (traditional_round_np,
                         sech_np, sech,
                         coth_np, coth,
                         cech_np, cech)
from .object_utils import (hash_code, gen_hash, safe_repr,
                           get_methods_and_attributes)
from .path_utils import (join_file_path,
                         sep_file_path,
                         list_files_with_suffix,
                         print_files_and_folders,
                         print_top_level_files_and_folders,
                         list_top_level_files_and_folders)
from .str_utils import (str_partition, )
from .typing_utils import (NumericArrayLike, is_numericarraylike)
from .unique_object import (unique_string,
                            random_string,
                            UniqueObject)

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
The common functions and classes of the gxusthjw python packages.
"""

__all__ = [
    'is_sorted',
    'is_sorted_ascending',
    'is_sorted_descending',
    'reverse',
    'is_equals_of',
    'Ordering',
    'sort',
    'DataCapsule',
    'ExceptionBase',
    'StateException',
    'get_file_encoding_chardet',
    'file_info',
    'get_file_info',
    'get_file_info_of_module',
    'get_file_object',
    'FileInfo',
    'FileObject',
    'read_txt',
    'Author',
    'Version',
    'Copyright',
    'Base',
    'traditional_round',
    'monotonic_linear',
    'monotonic_power',
    'monotonic_log',
    'NUMERICAL_PRECISION',
    'ARITHMETIC_PRECISION',
    'FLOAT_EPSILON',
    'TINY_FLOAT',
    'BOLTZMANN_CONSTANT',
    'GAS_CONSTANT',
    'AVOGADRO_CONSTANT',
    'float_epsilon',
    'traditional_round_np',
    'sech_np',
    'sech',
    'coth_np',
    'coth',
    'cech_np',
    'cech',
    'hash_code',
    'gen_hash',
    'safe_repr',
    'get_methods_and_attributes',
    'join_file_path',
    'sep_file_path',
    'list_files_with_suffix',
    'print_files_and_folders',
    'print_top_level_files_and_folders',
    'list_top_level_files_and_folders',
    'str_partition',
    'NumericArrayLike',
    'is_numericarraylike',
    'random_string',
    'unique_string',
    'UniqueObject',
]
# ==================================================================
