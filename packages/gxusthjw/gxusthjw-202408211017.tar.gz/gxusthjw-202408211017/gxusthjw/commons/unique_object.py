#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        unique_object.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义与“`独一无二`对象”相关的类和函数。
#                   Outer Parameters: xxxxxxx
# Class List:       UniqueObject -- 表征“独一无二对象”
# Function List:    random_string(length) -- 随机生成一个指定长度的字符串。
#                   unique_string() -- 生成一个具有一定唯一性的字符串。
#
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/07     revise
#       Jiwei Huang        0.0.1         2024/08/20     finish
# ------------------------------------------------------------------
# 导包 =============================================================
import random
import string
import time
import uuid
from typing import Tuple, Dict

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining the classes and functions associated with `unique object`.
"""

__all__ = [
    'random_string',
    'unique_string',
    'UniqueObject',
]


# 定义 ===============================================================

def random_string(length: int = 10) -> str:
    """
    随机生成一个指定长度的字符串。

    :param length: 要生成字符串的长度。
    :return: 生成的字符串。
    """
    # 定义字符集，包括小写字母、大写字母、数字和下划线
    characters = string.ascii_letters + string.digits + "_"
    # 使用random.choices从字符集中随机选择length个字符
    return ''.join(random.choices(characters, k=length))


def unique_string():
    """
    生成一个具有一定唯一性的字符串。

    :return:所生成的具有唯一性的字符串。
    """
    # 生成一个基于时间的 UUID，并将 UUID 转换为字符串形式
    unique_str = str(uuid.uuid1())
    # 添加当前时间戳
    timestamp = str(int(time.time()))
    # 返回一个包含 UUID 和时间戳的字符串
    return f"{unique_str}_{timestamp}"


class UniqueObject(object):
    """
    类`UniqueObject`表征“独一无二对象”。
    """

    # 用于确保标识符的唯一性。
    __identifier_set = set()

    def __init__(self, *args, **kwargs):
        """
        类`UniqueObject`的初始化方法。

        :param args: 可选参数，被保存为对象的args属性。
        :param kwargs: 可选关键字参数，将被全部转化为对象的属性。
        """
        _identifier = unique_string()
        while True:
            if _identifier not in UniqueObject.__identifier_set:
                UniqueObject.__identifier_set.add(_identifier)
                break
            else:
                _identifier = unique_string()
        self.__identifier = _identifier
        # 可选参数被保存为对象的args属性。
        self.__args = args
        # 可选关键字参数将被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def identifier(self) -> str:
        """
        获取对象的标识符。

        :return: 对象的标识符。
        """
        return self.__identifier

    @property
    def args(self) -> Tuple:
        """
        获取对象的可选参数。

        :return: 对象的可选参数。
        """
        return self.__args

    def get_arg(self, index: int):
        """
        获取指定索引的可选参数。

        :param index: 指定的索引。
        :return: 指定索引的可选参数。
        """
        return self.__args[index]

    @property
    def properties(self) -> Dict:
        """
        获取对象的所有属性。

        :return: 对象的所有属性。
        """
        res = dict()
        properties = vars(self)
        if len(properties) > 2:
            for prop_name, prop_value in properties.items():
                if prop_name.startswith('_UniqueObject'):
                    continue
                else:
                    res[prop_name] = prop_value
        return res

    # noinspection DuplicatedCode
    def __eq__(self, other_obj):
        """
        比较与另一个对象的相等性。

        因为对象的identifier是唯一的，
        所以此方法永远返回False。

        :param other_obj: 另一个对象。
        :return: 相等返回True，否则返回False。
        """
        # 获取第一个对象的属性名
        attrs1 = vars(self)
        attrs2 = vars(other_obj)

        # 检查两个对象的属性数量是否相同
        if len(attrs1) != len(attrs2):
            return False

        # 遍历第一个对象的属性
        for attr_name, attr_value in attrs1.items():
            # 如果属性名不存在于第二个对象或者值不相等，则返回 False
            if attr_name not in attrs2 or attrs2[attr_name] != attr_value:
                return False

        # 如果所有属性都相等，则返回 True
        return True

    def __ne__(self, other_obj):
        """
        比较与另一个对象的不相等性。

        因为对象的identifier是唯一的，
        所以此方法永远返回True。

        :param other_obj: 另一个对象。
        :return: 不相等返回True，否则返回False。
        """
        return not self.__eq__(other_obj)

    def __hash__(self):
        """
        获取对象的hashcode码。

        :return: 对象的hashcode码。
        """
        return hash(frozenset(vars(self).items()))

    # noinspection DuplicatedCode
    def __str__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        res = "UniqueObject({} = '{}'".format("identifier", self.__identifier)
        if len(self.args) > 0:
            res += ', args = {}'.format(self.args)
        properties = self.properties
        for prop_name, prop_value in properties.items():
            if isinstance(prop_value, (int, float)):
                res += ', {} = {}'.format(prop_name, prop_value)
            elif isinstance(prop_value, str):
                res += ', {} = \'{}\''.format(prop_name, prop_value)
            else:
                if prop_value is self:
                    res += '\n{} = {}'.format(prop_name, "self")
                else:
                    res += '\n{} = {}'.format(prop_name, str(prop_value))
        res += ')'
        return res

    # noinspection DuplicatedCode
    def __repr__(self):
        """
        获取对象字符串。

        :return: 对象字符串。
        """
        res = "UniqueObject({} = '{}'".format("identifier", self.__identifier)
        if len(self.args) > 0:
            res += ','
            res += ",".join(map(str, self.args))
        properties = self.properties
        for prop_name, prop_value in properties.items():
            if isinstance(prop_value, (int, float)):
                res += ', {} = {}'.format(prop_name, prop_value)
            elif isinstance(prop_value, str):
                res += ', {} = \'{}\''.format(prop_name, prop_value)
            else:
                if prop_value is self:
                    res += '\n{} = {}'.format(prop_name, "self")
                else:
                    res += '\n{} = {}'.format(prop_name, repr(prop_value))
        res += ')'
        return res
# ==================================================================
