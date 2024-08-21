#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        math_plus.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“补充`math`模块”的方法。
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
import math

# 声明  ==============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Defining the classes and functions for the supplementary math module.
"""
__all__ = [
    'traditional_round',
]


# 定义 ==================================================================

def traditional_round(value):
    """
    计算一个值四舍五入后的结果。

    Python提供有round函数，但其round(0.5)  ---> 0

    此函数使用了不同的规则，使得round(0.5)  ---> 1

    :param value: 需要四舍五入的值。
    :return: 四舍五入后的值。
    """
    res = math.floor(value)
    fraction = value - res
    if fraction >= 0.5:
        res = math.ceil(value)
    return res
