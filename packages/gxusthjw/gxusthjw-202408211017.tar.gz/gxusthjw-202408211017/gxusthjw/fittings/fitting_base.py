#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        fitting_base.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`拟合基类`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxx() -- xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/15     finish
# ------------------------------------------------------------------
# 导包 ==============================================================
import abc
from abc import abstractmethod

from typing import Optional, Union
import numpy as np
import numpy.typing as npt

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a base class that represents `fitting`.
"""

__all__ = [
    'FittingBase'
]


# 定义 ==============================================================

class FittingBase(metaclass=abc.ABCMeta):
    """
    类`FittingBase`表征“拟合基类”。
    """

    def __init__(self, y: npt.ArrayLike,
                 x: Optional[npt.ArrayLike] = None,
                 start: Optional[int] = None,
                 length: Optional[int] = None,
                 method: Optional[Union[str, int]] = None,
                 **kwargs):
        """
        类`FittingBase`的初始化方法。

        :param y: 因变量数据。
        :param x: 自变量数据。
        :param start: 要拟合数据的起始位置索引。
        :param length: 要拟合数据的长度。
        :param method: 拟合方法。
        :param kwargs: 其他可选关键字参数，将全部转化为对象的属性。
        """
        # 构造因变量数据。
        self.__y = np.asarray(y)
        self.__y_len = self.__y.shape[0]

        # 构造自变量数据。
        if x is None:
            self.__x = np.arange(self.__y_len)
        else:
            self.__x = np.asarray(x)
        self.__x_len = self.__x.shape[0]

        # 解析start
        if start is None:
            self.start = 0
        else:
            self.start = start

        # 解析length
        if length is None:
            _length = self.__x_len if self.__y_len >= self.__x_len else self.__y_len
            self.length = _length - self.start
        else:
            self.length = length

        # 解析method
        self.method = method

        # 可选关键字参数将被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def y(self) -> npt.NDArray:
        """
        获取因变量数据。

        :return: 因变量数据。
        """
        return self.__y

    @property
    def y_len(self) -> int:
        """
        获取因变量数据的长度。

        :return: 因变量数据的长度。
        """
        return self.__y_len

    @property
    def x(self) -> npt.NDArray:
        """
        获取自变量数据。

        :return: 自变量数据。
        """
        return self.__x

    @property
    def x_len(self) -> int:
        """
        获取自变量数据的长度。

        :return: 自变量数据的长度。
        """
        return self.__x_len

    @property
    def x_var(self):
        """
        获取自变量的拟合数据。

        :return: 自变量的拟合数据。
        """
        return self.x[self.start:self.start + self.length]

    @property
    def y_var(self):
        """
        获取因变量的拟合数据。

        :return: 因变量的拟合数据。
        """
        return self.y[self.start:self.start + self.length]

    def check_var(self):
        """
        检查拟合数据是否具有相同的长度。
            如果不具有相同的长度，则抛出ValueError异常。
        """
        if self.x_var.shape != self.y_var.shape:
            raise ValueError("self.x_var.shape != self.y_var.shape.")

    def is_var_aligned(self):
        """
        判断拟合数据是否具有相同的长度。

        :return: 如果具有相同的长度，返回True，否则返回False。
        """
        return self.x_var.shape != self.y_var.shape

    def var_len(self):
        """
        获取拟合数据的长度。

        :return: 拟合数据的长度。
        """
        self.check_var()
        return self.x_var.shape[0]

    # ------------------------------------------------------
    @abstractmethod
    def fit(self, **kwargs):
        """
        执行拟合。

        :param kwargs: 拟合所需的关键字参数。
        :return: 拟合结果，拟合统计对象。
        """
        pass

    @abstractmethod
    def interactive_fit(self, **kwargs):
        """
        交互式执行拟合。

        :param kwargs: 拟合所需的关键字参数。
        :return: 拟合结果，拟合统计对象。
        """
        pass

# ======================================================
