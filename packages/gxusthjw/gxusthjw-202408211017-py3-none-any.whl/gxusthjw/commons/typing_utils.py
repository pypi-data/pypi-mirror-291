#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        typing_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为`类型注解`提供工具函数和类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
from typing import Union, Iterable

import numpy as np
import numpy.typing as npt

# 声明 =============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining functions and classes for `typing (type annotations)`.
"""

__all__ = [
    'NumericArrayLike',
    'is_numericarraylike',
]

# 定义 ===============================================================

# 数值型类数组
NumericArrayLike = Union[npt.NDArray[np.number], Iterable[Union[int, float]]]
"""
数值型类数组。

几种类似的类型注解方式：

        1. npt.ArrayLike：这种方式无法说明元素类型为数值。

        2. Iterable[Union[int, float]：这种方式无法涵盖ndarray，
                                       尤其是ndarray中数值元素的类型有多种。

        3. npt.NDArray[Union[int, float]]：这种方式说明仅包括了int或float型的ndarray对象。
                                           然而，实质上ndarray中数值元素的类型有很多。

        4. npt.NDArray[np.number]：这种方式说明任意数值类型的ndarray对象。
"""


def is_numericarraylike(arr: NumericArrayLike) -> bool:
    """
    检查给定的对象是否符合 Union[npt.NDArray[np.number], Iterable[Union[int, float]]] 的要求。

    :param arr: 给定的对象。
    :return: 如果给定的对象符合要求，则返回 True；否则返回 False。
    """
    if isinstance(arr, np.ndarray):
        # 检查 numpy 数组中的元素是否为数字类型
        return arr.dtype.kind in ('i', 'f')
    elif isinstance(arr, Iterable):
        # 检查可迭代对象中的元素是否为整数或浮点数
        try:
            for item in arr:
                if not isinstance(item, (int, float)):
                    return False
            return True
        except TypeError:
            # 如果对象不是可迭代的，捕获 TypeError
            return False
    else:
        return False
