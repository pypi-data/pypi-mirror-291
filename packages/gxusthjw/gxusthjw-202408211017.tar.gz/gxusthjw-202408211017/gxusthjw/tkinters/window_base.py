#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        window_base.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2024/08/15
# Description:      Main Function: 定义“表征`窗口基类`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxx() -- xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2024/08/15     create
# ------------------------------------------------------------------
# 导包 ==============================================================
import os
import tkinter as tk

from ..commons import get_methods_and_attributes

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a base class that represents `window`.
"""

__all__ = [
    'WindowBase',
]


# 定义 ================================================================
class WindowBase(object):
    """
    类`WindowBase`表征“窗口基类”。
    """

    def __init__(self, master, **kwargs):
        """
        类`WindowBase`的初始化方法。

        :param master: 主窗口，(tk.Tk)。
        :param kwargs: 其他关键字参数，将被转化为对象的属性。
        """
        self.master = master
        self.top = tk.Toplevel(master)
        self.top_methods, self.top_attributes = get_methods_and_attributes(self.top)

        # 处理窗口图标。
        if 'icon_file' in kwargs:
            self.icon_file = kwargs.pop('icon_file')
            _, file_ext = os.path.splitext(self.icon_file)
            try:
                if file_ext == ".ico":
                    self.top.iconbitmap(self.icon_file)
                else:
                    self.top.iconphoto(True, tk.PhotoImage(file=self.icon_file))
            except tk.TclError:
                print("Failed to load the icon file.")

        keys = list(kwargs.keys())
        # 其余窗口属性，均基于kwargs设置。
        for key in keys:
            if key in self.top_methods:
                method = getattr(self.top, key)
                method(kwargs.pop(key))
            elif key in self.top_attributes:
                # 检查属性是否是 @property 装饰过的
                if hasattr(type(self.top), key) and isinstance(
                        getattr(type(self.top), key), property):
                    # 检查是否有 setter 方法
                    if hasattr(type(self.top), f"{key}.setter"):
                        # 使用 @property.setter 方法赋值
                        setattr(self.top, key, kwargs.pop(key))
                else:
                    # 使用普通的 setattr 方法赋值
                    setattr(self.top, key, kwargs.pop(key))
            else:
                pass

        # self.is_closed = True
        # self.is_hidden = False

        # 可选关键字参数将被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    def close(self):
        """
        关闭窗口。
        """
        self.top.destroy()

    def hide(self):
        """
        隐藏窗口。
        """
        self.top.withdraw()

    def show(self):
        """
        显示窗口。
        """
        self.top.deiconify()
# ====================================================================
