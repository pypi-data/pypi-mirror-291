#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        monotonic_functions.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义一些“单调函数”。
#                   Outer Parameters: xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/15     revise
#       Jiwei Huang        0.0.1         2026/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
import numpy as np
import numpy.typing as npt

# 声明 ==============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Define some "monotone functions".
"""
__all__ = [
    'monotonic_linear',
    'monotonic_power',
    'monotonic_log',
]


# 定义 ==================================================================
def monotonic_linear(x: npt.ArrayLike, a: float, b: float):
    """
    线性函数。

    形式：f(x) = a * x + b

         当a>0时，f(x)函数为单调递增。

         当a<0时，f(x)函数为单调递减。

         当a=0时，线性函数退化为常数函数 ，f(x) = b，
                 此时函数既不是单调递增也不是单调递减，
                 而是一个常数。

    :param x: 自变量。
    :param a: 参数a。
    :param b: 参数b。
    :return: 函数值。
    """
    return np.asarray(x) * a + b


def monotonic_power(x, a, b, c):
    """
    指数函数。

    形式：f(x) = a^x * b + c

    当a>1时，随着x的增加，a^x会增加，单调递增。

    当 0 < a < 1时，随着x的增加，a^x会减小，单调递减。

    b为负数时，函数f(x)的单调性与a^x相反。

    :param x: 自变量。
    :param a: 参数a。
    :param b: 参数b。
    :param c: 参数c。
    :return: 函数值。
    """
    return np.power(a, np.asarray(x)) * b + c


def monotonic_log(x, a, b, c):
    """
    对数函数.

    形式：f(x) = log_a(x) * b + c

    当a>1时，随着x的增加，a^x会增加，单调递增。

    当 0 < a < 1时，随着x的增加，a^x会减小，单调递减。

    b为负数时，函数f(x)的单调性与a^x相反。

    :param x: 自变量。
    :param a: 参数a。
    :param b: 参数b。
    :param c: 参数c。
    :return: 函数值。
    """
    return np.log(a) / np.log(np.asarray(x)) * b + c
