#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        str_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 承载“字符串”相关的函数和类。
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
from typing import Tuple

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Assembling classes and functions associated with `str`.
"""
__all__ = [
    'str_partition',
]


# 定义 ================================================================
def str_partition(s: str, delimiter: str) -> Tuple[str, str]:
    """
    将字符串分割为指定分隔符之前为一段（含指定的分隔符），
    分隔符之后为一段（不含指定的分隔符）。

    :param s: 要被分割的字符串。
    :param delimiter: 指定的分隔符。
    :return: (分割后的前段，分割后的后段)。
    """
    # 查找子字符串的位置
    index = s.find(delimiter)
    # 如果子字符串存在于原字符串中
    if index != -1:
        # 子字符串之前的部分，包括子字符串本身
        before = s[:index + len(delimiter)]
        # 子字符串之后的部分
        after = s[index + len(delimiter):]
        return before, after
    else:
        # 如果子字符串不存在，则返回原字符串和空字符串
        return s, ''
