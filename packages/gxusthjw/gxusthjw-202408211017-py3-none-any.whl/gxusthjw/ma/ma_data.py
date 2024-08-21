#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        ma_data.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`力学数据`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/18     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from typing import Union, Optional

import numpy as np
import numpy.typing as npt
from ..experiment import ExperimentalData

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `mechanical data`.
"""

__all__ = [
    'MechanicalData'
]


# ==================================================================

class MechanicalData(ExperimentalData):
    """
    类`MechanicalData`表征“力学数据”。

    力学数据包含如下数据项：

        1. 时间（times），单位：s。

        2. 位移（displacements），单位：mm。

        3. 力（forces），单位：cN。
    """

    def __init__(self, times: npt.ArrayLike,
                 displacements: npt.ArrayLike,
                 forces: npt.ArrayLike,
                 **kwargs):
        """
        类`MechanicalData`的初始化方法。

        可选关键字参数：

            1. time_unit：时间单位，可以指定`min`或`s`（忽略大小写）。
                          如果指定的为`min`，则将时间数据项乘以60，单位转变为`s`。
                          默认值为：`s`。

            2. displacement_unit：位移单位，可以指定`m`，`dm`，`cm`，`mm`（忽略大小写）。
                                如果指定的为`m`，则将位移数据项乘以1000，单位转变为`mm`。
                                如果指定的为`dm`，则将位移数据项乘以100，单位转变为`mm`。
                                如果指定的为`cm`，则将位移数据项乘以10，单位转变为`mm`。
                                默认值为：`mm`。

            3. force_unit：力单位，可以指定`N`，`cN`（忽略大小写）。
                                如果指定的为`N`，则将力数据项乘以100，单位转变为`cN`。
                                默认值为：`cN`。

            4.init_length：初始长度，可选。

            5.init_length_unit：初始长度单位，可以指定`m`，`dm`，`cm`，`mm`（忽略大小写）。
                                如果init_length不为None，则对其进行单位换算，最终的单位为`mm`。

            6.cross_area：截面积，可选。

            7.cross_area_unit： 截面积单位，可以指定`m^2`，`dm^2`，`cm^2`，`mm^2`（忽略大小写）。
                               如果cross_area不为None，则对其进行单位换算，最终的单位为`mm^2`。

        :param times: 时间数据项。
        :param displacements: 位移数据项。
        :param forces: 力数据项。
        :param kwargs: 可选关键字参数。
        """
        self.__times = np.asarray(times)
        self.__displacements = np.asarray(displacements)
        self.__forces = np.asarray(forces)
        self.__data_len = self.__times.shape[0]

        if (self.__displacements.shape[0] != self.__data_len or
                self.__forces.shape[0] != self.__data_len):
            raise ValueError("Expect data items (times,displacements,forces)"
                             " to be the same length.")

        # 数据编号。
        self.__nos = np.arange(1, self.__data_len + 1)

        # 单位设置与变换 --------------------------------------------------
        if 'time_unit' in kwargs:
            self.__time_unit = kwargs.pop('time_unit')
            if self.__time_unit.lower() == 'min':
                self.__times = self.__times * 60
                self.__time_unit = 's'
            elif self.__time_unit.lower() == 's':
                self.__time_unit = 's'
            else:
                raise ValueError("Expect time_unit to be 'min' or 's'.")
        else:
            self.__time_unit = 's'

        if 'displacement_unit' in kwargs:
            self.__displacement_unit = kwargs.pop('displacement_unit')
            if self.__displacement_unit.lower() == 'm':
                self.__displacements = self.__displacements * 1000
                self.__displacement_unit = 'mm'
            elif self.__displacement_unit.lower() == 'dm':
                self.__displacements = self.__displacements * 100
                self.__displacement_unit = 'mm'
            elif self.__displacement_unit.lower() == 'cm':
                self.__displacements = self.__displacements * 10
                self.__displacement_unit = 'mm'
            elif self.__displacement_unit.lower() == 'mm':
                self.__displacement_unit = 'mm'
            else:
                raise ValueError("Expect displacement_unit to be 'm' or 'dm' or 'cm' or 'mm'.")
        else:
            self.__displacement_unit = 'mm'

        if 'force_unit' in kwargs:
            self.__force_unit = kwargs.pop('force_unit')
            if self.__force_unit.lower() == 'n':
                self.__forces = self.__forces * 100
                self.__force_unit = 'cN'
            elif self.__force_unit.lower() == 'cn':
                self.__force_unit = 'cN'
            else:
                raise ValueError("Expect force_unit to be 'N' or 'cN'.")
        else:
            self.__force_unit = 'cN'

        if 'init_length' in kwargs:
            self.__init_length: Optional[Union[int | float]] = kwargs.pop('init_length')
        else:
            self.__init_length: Optional[Union[int | float]] = None

        if 'init_length_unit' in kwargs:
            self.__init_length_unit = kwargs.pop('init_length_unit')
            if self.__init_length is None:
                self.__init_length_unit = 'mm'
            else:
                if self.__init_length_unit.lower() == 'm':
                    self.__init_length = self.__init_length * 1000
                    self.__init_length_unit = 'mm'
                elif self.__init_length_unit.lower() == 'dm':
                    self.__init_length = self.__init_length * 100
                    self.__init_length_unit = 'mm'
                elif self.__init_length_unit.lower() == 'cm':
                    self.__init_length = self.__init_length * 10
                    self.__init_length_unit = 'mm'
                elif self.__init_length_unit.lower() == 'mm':
                    self.__init_length_unit = 'mm'
                else:
                    raise ValueError("Expect init_length_unit to be 'm' or 'dm' or 'cm' or 'mm'.")
        else:
            self.__init_length_unit = 'mm'

        if 'cross_area' in kwargs:
            self.__cross_area: Optional[Union[int | float]] = kwargs.pop('cross_area')
        else:
            self.__cross_area: Optional[Union[int | float]] = None

        if 'cross_area_unit' in kwargs:
            self.__cross_area_unit = kwargs.pop('cross_area_unit')
            if self.__cross_area is None:
                self.__cross_area_unit = 'mm^2'
            else:
                if self.__cross_area_unit.lower() == 'm^2':
                    self.__cross_area = self.__cross_area * 1e6
                    self.__cross_area_unit = 'mm^2'
                elif self.__cross_area_unit.lower() == 'dm^2':
                    self.__cross_area = self.__cross_area * 1e4
                    self.__cross_area_unit = 'mm^2'
                elif self.__cross_area_unit.lower() == 'cm^2':
                    self.__cross_area = self.__cross_area * 1e2
                    self.__cross_area_unit = 'mm^2'
                elif self.__cross_area_unit.lower() == 'mm^2':
                    self.__cross_area_unit = 'mm^2'
                else:
                    raise ValueError("Expect cross_area_unit to be 'm^2' or 'dm^2' or 'cm^2' or 'mm^2'.")
        else:
            self.__cross_area_unit = 'mm^2'

        # 设置数据项为不可变 -----------------------------------------------
        self.__times.flags.writeable = False
        self.__displacements.flags.writeable = False
        self.__forces.flags.writeable = False
        self.__nos.flags.writeable = False
        # ---------------------------------------------------------------

        super(MechanicalData, self).__init__(**kwargs)

    @property
    def times(self) -> npt.NDArray:
        """
        获取时间数据项（单位：s）。

        :return:时间数据项（单位：s）。
        """
        return self.__times

    @property
    def displacements(self) -> npt.NDArray:
        """
        获取位移数据项（单位：mm）。

        :return: 位移数据项（单位：mm）。
        """
        return self.__displacements

    @property
    def forces(self) -> npt.NDArray:
        """
        获取力数据项（单位：cN）。

        :return: 力数据项（单位：cN）。
        """
        return self.__forces

    @property
    def nos(self) -> npt.NDArray:
        """
        获取编号数据项。

        :return: 编号数据项。
        """
        return self.__nos

    @property
    def data_len(self) -> int:
        """
        获取数据长度。

        :return: 数据长度。
        """
        return self.__data_len

    @property
    def time_unit(self) -> str:
        """
        获取时间的单位。

        :return: 时间的单位。
        """
        return self.__time_unit

    @property
    def displacement_unit(self) -> str:
        """
        获取位移的单位。

        :return: 位移的单位。
        """
        return self.__displacement_unit

    @property
    def force_unit(self) -> str:
        """
        获取力数据的单位。

        :return: 力数据的单位。
        """
        return self.__force_unit

    @property
    def init_length(self) -> Optional[int | float]:
        """
        获取样品的初始长度。

        :return: 样品的初始长度。
        """
        return self.__init_length

    @property
    def init_length_unit(self) -> str:
        """
        获取样品的初始长度单位。

        :return: 初始长度单位。
        """
        return self.__init_length_unit

    @property
    def cross_area(self) -> Optional[int | float]:
        """
        获取样品的截面积。

        :return: 样品的截面积。
        """
        return self.__cross_area

    @property
    def cross_area_unit(self) -> str:
        """
        获取样品的截面积单位。

        :return: 样品的截面积单位。
        """
        return self.__cross_area_unit

    def set_init_length(self, init_length: Union[int, float],
                        init_length_unit: str):
        """
        设置样品的初始长度及其单位。

        :param init_length: 初始长度值。
        :param init_length_unit: 初始长度的单位。
        """
        self.__init_length = init_length
        self.__init_length_unit = init_length_unit
        if self.__init_length_unit.lower() == 'm':
            self.__init_length = self.__init_length * 1000
            self.__init_length_unit = 'mm'
        elif self.__init_length_unit.lower() == 'dm':
            self.__init_length = self.__init_length * 100
            self.__init_length_unit = 'mm'
        elif self.__init_length_unit.lower() == 'cm':
            self.__init_length = self.__init_length * 10
            self.__init_length_unit = 'mm'
        elif self.__init_length_unit.lower() == 'mm':
            self.__init_length_unit = 'mm'
        else:
            raise ValueError("Expect init_length_unit to be 'm' or 'dm' or 'cm' or 'mm'.")

    def set_cross_area(self, cross_area: Union[int, float],
                       cross_area_unit: str):
        """
        设置样品的截面积及其单位。

        :param cross_area: 截面积值。
        :param cross_area_unit: 截面积的单位。
        """
        self.__cross_area = cross_area
        self.__cross_area_unit = cross_area_unit
        # 单位变换。
        if self.__cross_area_unit.lower() == 'm^2':
            self.__cross_area = self.__cross_area * 1e6
            self.__cross_area_unit = 'mm^2'
        elif self.__cross_area_unit.lower() == 'dm^2':
            self.__cross_area = self.__cross_area * 1e4
            self.__cross_area_unit = 'mm^2'
        elif self.__cross_area_unit.lower() == 'cm^2':
            self.__cross_area = self.__cross_area * 1e2
            self.__cross_area_unit = 'mm^2'
        elif self.__cross_area_unit.lower() == 'mm^2':
            self.__cross_area_unit = 'mm^2'
        else:
            raise ValueError("Expect cross_area_unit to be 'm^2' or 'dm^2' or 'cm^2' or 'mm^2'.")
