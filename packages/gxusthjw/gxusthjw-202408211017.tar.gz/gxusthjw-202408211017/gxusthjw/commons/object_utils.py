#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        object_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 承载与`对象`有关的类和函数。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    hash_code(*args) -- 计算可变参数组的hash码。
#                   gen_hash(*args) -- 生成可变参数组的hash码。
#                   safe_repr(obj: object, short: bool = False,
#                             max_length: int = 80) --
#                             获取指定对象的__repr__信息值。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/01/01     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import inspect
from typing import Tuple, List

# 声明  ==============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Defining the classes and functions associated with `object`.
"""
__all__ = [
    'hash_code',
    'gen_hash',
    'safe_repr',
    'get_methods_and_attributes',
]


# 定义 ===============================================================
def hash_code(*args) -> int:
    """
    计算可变参数组的hash码。

    参考自：`java.util.Arrays.hashCode(Object ...args)`方法的算法。

    :param args: 可变参数组。
    :return: hash码。
    :rtype: `int`
    """
    if args is None:
        return 0

    result: int = 1
    for arg in args:
        result = 31 * result + (0 if arg is None else hash(arg))

    return result


def gen_hash(*args) -> int:
    """
    生成可变参数组的hash码。

    :param args: 可变参数组。
    :return: hash码。
    :rtype: `int`
    """
    return hash_code(*args)


def safe_repr(obj: object, short: bool = False,
              max_length: int = 80) -> str:
    """
    获取指定对象的__repr__信息值。

    :param obj: 指定的对象。
    :param short: 是否简短信息，True表示简短信息，False表示不简短信息。
    :param max_length: 若简短信息，则此值指定允许信息的最大长度。
    :return: 对象的__repr__信息值。
    """
    # noinspection PyBroadException
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < max_length:
        return result
    return result[:max_length] + ' [truncated]...'


def get_methods_and_attributes(obj) -> Tuple[List, List]:
    """
    获取指定对象的所有方法和属性。

    实现概述：
        1. dir() 函数：dir(obj) 返回对象的所有属性和方法的列表。
        2. 使用 member.startswith("_")过滤掉约定内部使用的方法，
            inspect.ismethod() 判断是否为方法。
        3. 使用 not member.startswith("__") 排除特殊方法（如 __str__）。
        4. 使用 not inspect.isroutine() 排除特殊方法和内置函数。

    :param obj: 指定的对象。
    :return: 方法列表，属性列表。
    """
    methods = list()
    attributes = list()
    # 获取所有方法和属性
    all_members = dir(obj)
    for member in all_members:
        if member.startswith("_") or member.startswith("__"):
            continue
        if inspect.ismethod(getattr(obj, member)):
            methods.append(member)
        elif not inspect.isroutine(getattr(obj, member)):
            attributes.append(member)
        else:
            pass
    return methods, attributes
