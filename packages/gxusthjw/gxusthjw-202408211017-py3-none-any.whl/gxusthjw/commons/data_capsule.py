#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        data_capsule.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`数据容器(数据囊)`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       DataCapsule -- 表征“数据容器(数据囊)”。
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/12/30     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     finish
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Optional, Union, Tuple

import numpy as np
import pandas as pd

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents a `data container (data capsule)`.
"""

__all__ = [
    'DataCapsule'
]

# 定义 ===============================================================
# 缺省的数据项名前缀。
__DEFAULT_ITEM_NAME_PREFIX__ = "item_"


class DataCapsule(object):
    """
    类`DataCapsule`表征“数据容器(数据囊)”。

    在`DataCapsule`对象中，保存了各种不同类型的“数据项”，
    每个数据项均有一个数据项名和数据项数据组成。
    """

    def __init__(self, *args, **kwargs):
        """
        类`DataCapsule`的初始化方法。

            1. 对于可选参数args，其作用是指定数据项的数据，args中的每个元素为1条数据项的数据。

                args中每个元素的允许值包括：

                （1）标量值，类型必须为int,float,bool,str或object等。

                （2）类数组值： 类型必须为list，tuple，numpy.ndarray等。

            2. 对于可选关键字参数kwargs，其作用是指定数据项的名称及其他关键字参数：

                （1）通过item_names关键字参数，如果其为字典，则键对应数据项的序号，
                    而值对应数据项名。

                （2）通过item_names关键字参数，如果其为列表或元组，则序号对应数据项的序号，
                    而值对应数据项名。

                （3）如果没有指定item_names关键字参数或者 item_names不符合（1）和（2）的规则，
                    则采用缺省的数据项名（item_i的形式）。

                （4）任何数据项名的遗漏，都会以item_i的形式代替。

            3. 对于可选关键字参数kwargs，除item_names外，其余所有关键字参数均被转化为对象的属性。

        :param args: 可选参数，元组类型，用于初始化”数据项“的数据。
        :param kwargs: 可选的关键字参数，字典类型，
                       用于初始化”数据项“的名称及其他属性参数。
        """
        # 数据容器(数据囊)对象中的数据被保存为pandas.DataFrame格式。
        # 私有实例变量`__data`用于保存数据容器(数据囊)对象中的数据。
        self.__data = pd.DataFrame()

        # 根据指定的参数，更新数据容器(数据囊)对象。
        self.update_data(*args, **kwargs)

    @property
    def is_empty(self) -> bool:
        """
        判断数据容器(数据囊)是否为空。

        :return: 如果数据容器(数据囊)为空，则返回True，否则返回False。
        """
        return self.__data.empty

    @property
    def shape(self) -> Tuple[int, int]:
        """
        获取数据容器(数据囊)的形状。

        :return: 元组（行数，列数）。
        """
        return self.__data.shape

    def update_data(self, *args, **kwargs):
        """
        更新或添加数据项。

            1. 对于可选参数args，其作用是指定数据项的数据，args中的每个元素为1条数据项的数据。

                args中每个元素的允许值包括：

                （1）标量值，类型必须为int,float,bool,str或object等。

                （2）类数组值： 类型必须为list，tuple，numpy.ndarray等。

            2. 对于可选关键字参数kwargs，其作用是指定数据项的名称及其他关键字参数：

                （1）通过item_names关键字参数，如果其为字典，则键对应数据项的序号，
                    而值对应数据项名。

                （2）通过item_names关键字参数，如果其为列表或元组，则序号对应数据项的序号，
                    而值对应数据项名。

                （3）如果没有指定item_names关键字参数或者 item_names不符合（1）和（2）的规则，
                    则采用缺省的数据项名（item_i的形式）。

                （4）任何数据项名的遗漏，都会以item_i的形式代替。

            3. 对于可选关键字参数kwargs，除item_names外，其余所有关键字参数均被转化为对象的属性。

        :param args: 可选参数，元组类型，用于初始化”数据项“的数据。
        :param kwargs: 可选的关键字参数，字典类型，
                       用于初始化”数据项“的名称及其他属性参数。
        """
        # 初始数据项数。
        item_count = len(args)

        # 初始数据项名。
        item_names = {}

        # 构建数据项名。
        if "item_names" in kwargs and kwargs["item_names"] is not None:
            kwargs_item_names = kwargs["item_names"]

            # 如果指定数据项名时，使用的是字典。
            if isinstance(kwargs_item_names, dict):
                for key in kwargs_item_names.keys():
                    # 字典的键必须是整数，这个整数代表数据项的序号。
                    if not isinstance(key, int):
                        raise ValueError("the key of item_names must be a int value,"
                                         "but got {}".format(key))
                    # 如果键值超过了初始数据项的数量，则跳过。
                    if key >= item_count:
                        continue
                    key_item_name = kwargs_item_names[key]
                    # 如果字典值类型不是None，则设置为数据项名。
                    if key_item_name is not None:
                        if isinstance(key_item_name, str):
                            item_names[key] = key_item_name
                        else:
                            item_names[key] = str(key_item_name)
                    else:
                        item_names[key] = "{}{}".format(
                            __DEFAULT_ITEM_NAME_PREFIX__, key)
            # 如果指定数据项名时，使用的是列表或元组。
            elif isinstance(kwargs_item_names, (list, tuple)):
                for item_index in range(len(kwargs_item_names)):
                    if item_index >= item_count:
                        break
                    item_name = kwargs_item_names[item_index]
                    if item_name is not None:
                        if isinstance(item_name, str):
                            item_names[item_index] = item_name
                        else:
                            item_names[item_index] = str(item_name)
                    else:
                        item_names[item_index] = "{}{}".format(
                            __DEFAULT_ITEM_NAME_PREFIX__, item_index)
            else:
                raise ValueError("The type of item_names must be one of {{dict,list,tuple}}")
        else:
            current_item_index = self.shape[1]
            for item_index in range(item_count):
                item_names[item_index] = "{}{}".format(
                    __DEFAULT_ITEM_NAME_PREFIX__, current_item_index + item_index)

        # 补充遗漏
        for item_index in range(item_count):
            if item_index in item_names.keys():
                continue
            else:
                item_names[item_index] = "{}{}".format(
                    __DEFAULT_ITEM_NAME_PREFIX__, item_index)

        # 初始化数据。
        if len(item_names) != 0:
            make_list = list()
            make_list.append(self.__data)
            for item_index in range(item_count):
                item_value = args[item_index]
                # 如果指定数据项名的数据项已经存在，则删除之。
                if item_names[item_index] in self.__data.columns:
                    del self.__data[item_names[item_index]]

                # 检查args[i]是否为标量，如果是，在构造DataFrame时，必须给index
                if np.isscalar(item_value):
                    make_list.append(pd.DataFrame({item_names[item_index]: item_value}, index=[0]))
                elif isinstance(item_value, (list, tuple, pd.Series, np.ndarray)):
                    # make_list.append(pd.DataFrame({col_names[col_index]: np.array(col_value, copy=True)}))
                    make_list.append(pd.DataFrame({item_names[item_index]: item_value}))
                else:
                    make_list.append(pd.DataFrame({item_names[item_index]: [item_value, ]}, index=[0]))
            self.__data = pd.concat(make_list, axis=1)

        # 其他关键字参数将被转换为对象的属性。
        for key in kwargs.keys():
            if hasattr(self, key) or "item_names".__eq__(key):
                continue
            else:
                setattr(self, key, kwargs[key])

    def update_item(self, item_data, item_name: Optional[str] = None):
        """
        更新或添加数据项。

        :param item_data: 要更新或添加的数据项数据。
        :param item_name: 要更新或添加的数据项名。
        """
        if item_name is None:
            num_col = self.shape[1]
            item_name = "{}{}".format(__DEFAULT_ITEM_NAME_PREFIX__, num_col)

        if not isinstance(item_name, str):
            raise ValueError("the type of col_name must be a str,"
                             "but got {}.".format(item_name))

        if item_name in self.__data.columns:
            del self.__data[item_name]

        if np.isscalar(item_data):
            new_frame = pd.DataFrame({item_name: item_data}, index=[0])
        elif isinstance(item_data, (list, tuple, pd.Series, np.ndarray)):
            new_frame = pd.DataFrame({item_name: item_data})
        else:
            new_frame = pd.DataFrame({item_name: [item_data, ]}, index=[0])

        # 判断self.__data是否为空。
        if len(self.__data.index) == 0:
            self.__data = new_frame
        else:
            self.__data = pd.concat([self.__data, new_frame], axis=1)

    def get_item(self, col_index: Union[str, int]):
        """
        获取指定索引的数据项。

        :param col_index: 索引。
        :return: 数据项。
        """
        if isinstance(col_index, int):
            return self.__data.iloc[:, col_index].dropna()
        else:
            return self.__data[col_index].dropna()

    def print_data(self, options: Optional[dict] = None):
        """
        print数据。

        :param options: 用于设置set_option的键和值。
        """
        if options:
            for key in options.keys():
                pd.set_option(key, options[key])

        print(self.__data)

    @property
    def data(self) -> pd.DataFrame:
        """
        获取数据容器（数据囊）的深度copy。

        :return: 数据容器（数据囊）的深度copy。
        """
        return self.__data.copy(deep=True)

    def to_csv(self, **kwargs):
        """
        数据输出至csv格式文件。

        :param kwargs: pandas.to_csv方法所需的关键字参数。
        :return: pandas.to_csv方法的返回值。
        """
        return self.__data.to_csv(**kwargs)

    def to_excel(self, excel_writer, **kwargs):
        """
        数据输出至excel格式文件。

        :param excel_writer: path-like, file-like, or ExcelWriter object
            File path or existing ExcelWriter.
        :param kwargs: pandas.to_excel方法所需的关键字参数。
        """
        self.__data.to_excel(excel_writer, **kwargs)

    def to_dict(self, **kwargs):
        """
        数据转换为dict.

        :param kwargs:pandas.to_dict方法所需的关键字参数。
        :return: dict对象。
        """
        return self.__data.to_dict(**kwargs)
