#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        experimental_data.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`实验数据`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/18     finish
# ----------------------------------------------------------------
# 导包 ============================================================

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents `experimental data`.
"""

__all__ = [
    'ExperimentalData',
]


# ==================================================================
class ExperimentalData(object):
    """
    类`ExperimentalData`表征“实验数据”。

    类`ExperimentalData`实质上是一个基类，所有表征实验数据的类均应继承自此类。

    所有表征实验数据的对象均拥有2个基本属性：

        1. 样品名（specimen_name）。

        2. 测试编号（specimen_no）。

    而样品名与测试编号可合并得到：

        1. 数据名称（sample_name）：样品名_测试编号。
    """

    def __init__(self, **kwargs):
        """
        类`ExperimentalData`的构造方法。

            用到的关键字参数如下：

            1. specimen_name：样品名，缺省值为：‘specimen’。

            2. specimen_no：测试编号，缺省值为：0。

            其他未用到的关键字参数，同样将被全部转化为对象的属性。

        :param kwargs: 其他关键字参数，将全部转化为对象的属性。
        """
        # 样品名。
        if 'specimen_name' in kwargs:
            self.__specimen_name: str = kwargs.pop('specimen_name')
        else:
            self.__specimen_name: str = 'specimen'

        # 测试编号。
        if 'specimen_no' in kwargs:
            self.__specimen_no: int = kwargs.pop('specimen_no')
        else:
            self.__specimen_no: int = 0

        # 可选关键字参数将被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def specimen_name(self) -> str:
        """
        获取样品名。

        :return: 样品名。
        """
        return self.__specimen_name

    @specimen_name.setter
    def specimen_name(self, value: str):
        """
        设置样品名。

        :param value: 样品名。
        """
        self.__specimen_name = value

    @property
    def specimen_no(self) -> int:
        """
        获取测试编号。

        :return: 测试编号。
        """
        return self.__specimen_no

    @specimen_no.setter
    def specimen_no(self, value: int):
        """
        设置测试编号。

        :param value: 测试编号。
        """
        self.__specimen_no = value

    @property
    def sample_name(self) -> str:
        """
        获取测试数据的名称。

        :return: 测试数据的名称。
        """
        return "{}_{}".format(self.specimen_name, self.specimen_no)

# ===================================================================
