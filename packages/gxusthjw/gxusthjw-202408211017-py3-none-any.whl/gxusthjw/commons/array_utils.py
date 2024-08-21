#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        array_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为`类似数组`的对象提供辅助方法和类。
#                   Outer Parameters: xxxxxxx
# Class List:       Ordering -- 枚举`Ordering`表征有序性。
# Function List:    is_sorted(arr) --
#                                              判断指定的值组是否为有序的。
#                   is_sorted_ascending(arr) --
#                                              判断指定的值组是否为升序的。
#                   is_sorted_descending(arr) --
#                                              判断指定的值组是否为降序的。
#                   reverse(arr) -- 将指定的值组倒置。
#                   is_equals_of(arr1,arr2,rtol=0, atol=1e-9) --
#                                              判断两个数组的相等性。
#                   sort(arr,ordering) -- 获取给定数值组的有序copy。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
from typing import Union
from enum import Enum
import numpy as np
import numpy.typing as npt

from .typing_utils import NumericArrayLike

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining helper functions and classes for `array-like` objects.
"""

__all__ = [
    'is_sorted',
    'is_sorted_ascending',
    'is_sorted_descending',
    'reverse',
    'is_equals_of',
    'Ordering',
    'sort'
]


# 定义 =================================================================
def is_sorted(arr: NumericArrayLike) -> bool:
    """
    判断给定的数值组是否为有序排列（升序或降序）。

    如果给定的数值组是有序的，则返回 True；否则返回 False。

    :param arr: 给定的数值组。
    :return: 如果给定的数值组是有序的，则返回 True；否则返回 False。
    """
    value_arr = np.asarray(arr)
    return (np.all(np.diff(value_arr) >= 0) or
            np.all(np.diff(value_arr) <= 0))


def is_sorted_ascending(arr: NumericArrayLike) -> bool:
    """
    判断给定的数值组是否为升序的。

    如果给定的数值组是是升序的，返回True，否则返回False。

    :param arr: 给定的数值组。
    :return:如果给定的数值组是是升序的，返回True，否则返回False。
    """
    value_arr = np.asarray(arr)
    return np.all(np.diff(value_arr) >= 0)


def is_sorted_descending(arr: NumericArrayLike) -> bool:
    """
    判断给定的数值组是否为降序的。

    如果给定的数值组是是降序的，返回True，否则返回False。

    :param arr: 给定的数值组。
    :return:如果给定的数值组是是降序的，返回True，否则返回False。
    """
    value_arr = np.asarray(arr)
    return np.all(np.diff(value_arr) <= 0)


def reverse(arr: NumericArrayLike) -> npt.NDArray[np.number]:
    """
    将给定的数值组倒置。

    :param arr: 给定的数值组。
    :return: 倒置后的数值组。
    """
    value_arr = np.asarray(arr)
    return np.array(value_arr[::-1], copy=True)


def is_equals_of(arr1: NumericArrayLike,
                 arr2: NumericArrayLike,
                 rtol=0, atol=1e-9) -> bool:
    """
    判断给定的两个数值组的相等性。

    第1个参数记为：a

    第2个参数记为：b

    则下式为True，此函数返回True：

        absolute(a - b) <= (atol + rtol * absolute(b))

    :param arr1: 数值组1。
    :param arr2: 数值组2。
    :param rtol: 相对容差，相对容差是指：两个数之差除以第2个数。
    :param atol: 绝对容差，绝对容差是指：两个数之差。
    :return:如果给定的两个数值组相等，则返回True，否则返回false。
    """
    return np.allclose(np.asarray(arr1), np.asarray(arr2),
                       rtol=rtol, atol=atol,
                       equal_nan=True)


class Ordering(Enum):
    """
    枚举`Ordering`表征有序性。
    """

    # 无序。
    UNORDERED = 0
    """
    ‘UNORDERED’表征`无序`。
    """

    # 升序。
    ASCENDING = 1
    """
    ‘ASCENDING’表征`升序`。
    """

    # 降序。
    DESCENDING = 2
    """
    ‘DESCENDING’表征`降序`。
    """

    # noinspection DuplicatedCode
    @staticmethod
    def of(value: Union[int, str]):
        """
        从值或成员名（忽略大小写）构建枚举实例。

        :param value: 指定的值或成员名（忽略大小写）。
        :return: Ordering对象。
        :rtype: Ordering
        """
        if isinstance(value, str):
            if value.upper() in Ordering.__members__:
                return Ordering.__members__[value]
            else:
                raise ValueError(f"Unknown value ({value}) for Ordering.")
        elif isinstance(value, int):
            for member in Ordering:
                if member.value == value:
                    return member
            raise ValueError(f"Unknown value ({value}) for Ordering.")
        else:
            raise ValueError(f"Unknown value ({value}) for Ordering.")


def sort(arr: NumericArrayLike,
         ordering: Ordering = Ordering.ASCENDING) -> npt.NDArray[np.number]:
    """
    获取给定数值组的有序copy。

    :param arr: 给定的数值组。
    :param ordering: 指定升序或降序。
    :return: 有序的数值组。
    """
    arr_sorted = np.sort(arr)
    if ordering == Ordering.DESCENDING:
        return reverse(arr_sorted)
    return arr_sorted
