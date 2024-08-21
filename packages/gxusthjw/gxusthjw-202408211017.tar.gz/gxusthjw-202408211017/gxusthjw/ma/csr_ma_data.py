#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        csr_ma_data.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`恒（常）应变速率力学数据`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/17     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from typing import Optional, Tuple

import numpy as np
import numpy.typing as npt

from .ma_data import MechanicalData

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `mechanical data of constant strain rate`.
"""

__all__ = [
    'CsrMechanicalData'
]


# ==================================================================

class CsrMechanicalData(MechanicalData):
    """
    类`CsrMechanicalData`表征“恒（常）应变速率（constant strain rate）力学数据”。
    """

    def __init__(self, times: npt.ArrayLike,
                 displacements: npt.ArrayLike,
                 forces: npt.ArrayLike,
                 **kwargs):
        """
        类`CsrMechanicalData`的初始化方法。

        :param times: 时间数据项。
        :param displacements: 位移数据项。
        :param forces: 力数据项。
        :param kwargs: 可选关键字参数。
        """
        # 应变速率（拉伸速度）。
        if 'strain_rate' not in kwargs:
            self.__strain_rate = kwargs.pop('strain_rate')
        else:
            self.__strain_rate = None

        if 'strain_rate_unit' in kwargs:
            self.__strain_rate_unit = kwargs.pop('strain_rate_unit')
            if self.__strain_rate is None:
                self.__strain_rate_unit = "mm/s"
            else:
                if self.__strain_rate_unit.lower() == "m/min":
                    self.__strain_rate = self.__strain_rate * 1000 / 60
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "dm/min":
                    self.__strain_rate = self.__strain_rate * 100 / 60
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "cm/min":
                    self.__strain_rate = self.__strain_rate * 10 / 60
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "mm/min":
                    self.__strain_rate = self.__strain_rate / 60
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "m/s":
                    self.__strain_rate = self.__strain_rate * 1000
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "dm/s":
                    self.__strain_rate = self.__strain_rate * 100
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "cm/s":
                    self.__strain_rate = self.__strain_rate * 10
                    self.__strain_rate_unit = "mm/s"
                elif self.__strain_rate_unit.lower() == "mm/s":
                    self.__strain_rate_unit = "mm/s"
                else:
                    raise ValueError("Expect cross_area_unit to be 'm/min' or 'dm/min' or"
                                     " 'cm/min' or 'mm/min' or 'm/s' or 'dm/s' or 'cm/s' or"
                                     " 'mm/s'.")
        else:
            self.__strain_rate_unit = "mm/s"

        super(CsrMechanicalData, self).__init__(times, displacements, forces, **kwargs)

    @property
    def strain_rate(self) -> Optional[int | float]:
        """
        获取应变率值。

        :return: 应变率值。
        """
        return self.__strain_rate

    @property
    def strain_rate_unit(self) -> str:
        """
        获取应变率单位。

        :return: 应变率单位。
        """
        return self.__strain_rate_unit

    def set_strain_rate(self, strain_rate, strain_rate_unit):
        """
        设置应变率及其单位。

        :param strain_rate: 应变率值。
        :param strain_rate_unit:  应变率单位。
        """
        self.__strain_rate = strain_rate
        self.__strain_rate_unit = strain_rate_unit
        if self.__strain_rate_unit.lower() == "m/min":
            self.__strain_rate = self.__strain_rate * 1000 / 60
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "dm/min":
            self.__strain_rate = self.__strain_rate * 100 / 60
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "cm/min":
            self.__strain_rate = self.__strain_rate * 10 / 60
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "mm/min":
            self.__strain_rate = self.__strain_rate / 60
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "m/s":
            self.__strain_rate = self.__strain_rate * 1000
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "dm/s":
            self.__strain_rate = self.__strain_rate * 100
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "cm/s":
            self.__strain_rate = self.__strain_rate * 10
            self.__strain_rate_unit = "mm/s"
        elif self.__strain_rate_unit.lower() == "mm/s":
            self.__strain_rate_unit = "mm/s"
        else:
            raise ValueError("Expect cross_area_unit to be 'm/min' or 'dm/min' or"
                             " 'cm/min' or 'mm/min' or 'm/s' or 'dm/s' or 'cm/s' or"
                             " 'mm/s'.")

    # -------------------------------------------------------------------------
    def time_fit(self, **kwargs):
        """
        对时间数据进行拟合处理。

        :param kwargs: 用到的关键字参数。
        """
        pass

    def displacement_fit(self, **kwargs):
        """
        对位移数据进行拟合处理。

        :param kwargs: 用到的关键字参数。
        """
        pass

    def forces_fit(self, **kwargs):
        """
        对力数据进行平滑处理。

        :param kwargs: 用到的关键字参数。
        """
        pass

    # -------------------------------------------------------------------------

    def strains(self, **kwargs) -> npt.NDArray:
        """
        计算应变数据。

        :param kwargs: 用到的关键字参数。
        :return: 应变数据。
        """
        pass

    def strain_rates(self, **kwargs) -> npt.NDArray:
        """
        计算应变率数据。

        :param kwargs: 用到的关键字参数。
        :return: 应变率数据。
        """
        return self.strains(**kwargs) * 100

    def stress(self, **kwargs) -> npt.NDArray:
        """
        计算应力数据。

        :param kwargs: 用到的关键字参数。
        :return: 应力数据。
        """
        pass

    # -------------------------------------------------------------------------
    def initial_modulus(self, **kwargs) -> float:
        """
        计算初始模量。

        :param kwargs: 用到的关键字参数。
        :return: 初始模量。
        """
        pass

    def strength(self, **kwargs) -> float:
        """
        计算断裂强度。

        :param kwargs: 用到的关键字参数。
        :return: 断裂强度。
        """
        pass

    def elongation(self, **kwargs) -> float:
        """
        计算断裂伸长率。

        :param kwargs: 用到的关键字参数。
        :return: 断裂伸长率。
        """
        pass

    def yield_point(self, **kwargs) -> Tuple[float, float]:
        """
        计算屈服点。

        :param kwargs: 用到的关键字参数。
        :return: 屈服点。
        """
        pass

    def hardening_point(self, **kwargs) -> Tuple[float, float]:
        """
        计算硬化点。

        :param kwargs: 用到的关键字参数。
        :return: 硬化点。
        """
        pass
    # -------------------------------------------------------------------------
