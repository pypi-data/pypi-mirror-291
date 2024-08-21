#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        numpy_plus.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“补充`numpy`模块”的方法。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import numpy as np
import numpy.typing as npt

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining the classes and functions for the supplementary numpy module.
"""

__all__ = [
    'traditional_round_np',
    'sech_np',
    'sech',
    'coth_np',
    'coth',
    'cech_np',
    'cech',
]


# 定义 ==================================================================
def traditional_round_np(x: npt.ArrayLike):
    """
    实现传统的四舍五入规则。

    当数值的小数部分大于等于 0.5 时，向远离零的方向舍入；
    小于 0.5 时，向最接近的整数舍入。

    :param x: 需要四舍五入的数组
    :return: 四舍五入后的数组
    """
    floor_array = np.floor(np.asarray(x))
    fraction = x - floor_array
    ceil_mask = fraction >= 0.5
    result = np.where(ceil_mask, np.ceil(x), floor_array)
    return result


def sech_np(x: npt.ArrayLike, *args, **kwargs):
    """
    基于numpy.cosh函数（双曲余弦），针对参数x的元素计算其双曲正割。

    :param x:array_like，Input array.
    :param args: 可以指定2个可选参数：
                 1. out：ndarray, None, or tuple of ndarray and None, optional
                        用于存储计算结果。
                        如果提供，它必须具有与输入变量广播到的形状相同。
                        如果未提供或为None，则返回一个新分配的数组。
                        元组(可能仅作为关键字参数)的长度必须等于输出的数量。
                 2. where：array_like, optional
                         针对输入数组x，在条件为True的位置，
                         out数组将被设置为ufunc结果。在其他地方，out数组将保留其原始值。
                         请注意，如果通过默认out=None创建未初始化的out数组，
                         则其中条件为False的位置将保持未初始化。
    :return:双曲正割
    """
    return 1.0 / np.cosh(x, *args, **kwargs)


def sech(x: npt.ArrayLike):
    """
    计算指定自变量组x的双曲正割。

    :param x: array_like，Input array.
    :return: 双曲正割
    """
    return 2.0 / (np.exp(x) + np.exp(-x))


def coth_np(x: npt.ArrayLike, *args, **kwargs):
    """
    基于numpy.tanh函数（双曲正切），针对参数x的元素计算其双曲余切。

    :param x:array_like，Input array.
    :param args: 可以指定2个可选参数：
                 1. out：ndarray, None, or tuple of ndarray and None, optional
                        用于存储计算结果。
                        如果提供，它必须具有与输入变量广播到的形状相同。
                        如果未提供或为None，则返回一个新分配的数组。
                        元组(可能仅作为关键字参数)的长度必须等于输出的数量。
                 2. where：array_like, optional
                         针对输入数组x，在条件为True的位置，
                         out数组将被设置为ufunc结果。在其他地方，out数组将保留其原始值。
                         请注意，如果通过默认out=None创建未初始化的out数组，
                         则其中条件为False的位置将保持未初始化。
    :return:双曲余切
    """
    return 1.0 / np.tanh(x, *args, **kwargs)


def coth(x: npt.ArrayLike):
    """
    计算指定自变量组x的双曲余切。

    :param x: array_like，Input array.
    :return: 双曲余切
    """
    return (np.exp(x) + np.exp(-x)) / (np.exp(x) - np.exp(-x))


def cech_np(x: npt.ArrayLike, *args, **kwargs):
    """
    基于numpy.sinh函数（双曲正弦），针对参数x的元素计算其双曲余割。

    :param x:array_like，Input array.
    :param args: 可以指定2个可选参数：
                 1. out：ndarray, None, or tuple of ndarray and None, optional
                        用于存储计算结果。
                        如果提供，它必须具有与输入变量广播到的形状相同。
                        如果未提供或为None，则返回一个新分配的数组。
                        元组(可能仅作为关键字参数)的长度必须等于输出的数量。
                 2. where：array_like, optional
                         针对输入数组x，在条件为True的位置，
                         out数组将被设置为ufunc结果。在其他地方，out数组将保留其原始值。
                         请注意，如果通过默认out=None创建未初始化的out数组，
                         则其中条件为False的位置将保持未初始化。
    :return:双曲余割。
    """
    return 1.0 / np.sinh(x, *args, **kwargs)


def cech(x: npt.ArrayLike):
    """
    计算指定自变量组x的双曲余割。

    :param x: array_like，Input array.
    :return: 双曲余割。
    """
    return 2.0 / (np.exp(x) - np.exp(-x))


def safe_slice(array: npt.NDArray, start: int, stop: int) -> npt.ArrayLike:
    """
    安全地对NumPy数组进行切片。

    如果提供的索引超出数组的边界，则抛出IndexError。

    :param array: NumPy数组
    :param start: 切片的起始索引
    :param stop: 切片的结束索引
    :return: 切片后的数组
    """
    if not 0 <= start < array.size or not 0 <= stop <= array.size:
        raise IndexError("Slice indices out of bounds")

    if start >= stop:
        raise ValueError("Start index must be less than stop index")

    return array[start:stop]
