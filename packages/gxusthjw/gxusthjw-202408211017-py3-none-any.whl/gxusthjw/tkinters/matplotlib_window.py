#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        matplotlib_window.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2024/08/15
# Description:      Main Function: 定义“表征`matplotlib窗口`”的类。
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
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ..commons import get_methods_and_attributes
from .window_base import WindowBase

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `matplotlib window`.
"""

__all__ = [
    'MatplotlibWindow',
]


# 定义 ================================================================
class MatplotlibWindow(WindowBase):
    """
    类`MatplotlibWindow`表征“matplotlib窗口”。
    """

    def __init__(self, master, **kwargs):
        """
        类`MatplotlibWindow`的初始化方法。

        :param master: 主窗口，(tk.Tk)。
        :param kwargs: 其他关键字参数，将被转化为对象的属性。
        """
        # 创建一个Figure实例
        self.fig = Figure()

        self.fig_methods, self.fig_attributes = get_methods_and_attributes(self.fig)

        keys = list(kwargs.keys())
        # 其余fig属性，均基于kwargs设置。
        for key in keys:
            if key in self.fig_methods:
                method = getattr(self.fig, key)
                method(kwargs.pop(key))
            elif key in self.fig_attributes:
                # 检查属性是否是 @property 装饰过的
                if hasattr(type(self.fig), key) and isinstance(
                        getattr(type(self.fig), key), property):
                    # 检查是否有 setter 方法
                    if hasattr(type(self.fig), f"{key}.setter"):
                        # 使用 @property.setter 方法赋值
                        setattr(self.fig, key, kwargs.pop(key))
                else:
                    # 使用普通的 setattr 方法赋值
                    setattr(self.fig, key, kwargs.pop(key))
            else:
                pass

        super(MatplotlibWindow, self).__init__(master, **kwargs)

        # 创建FigureCanvasTkAgg对象
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.top)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear_figure(self):
        """
        清除图表。
        """
        self.fig.clf()

    def draw_canvas(self):
        """
        重回画布。
        """
        self.canvas.draw()

    def plot(self, *args, **kwargs):
        """
        在窗口中绘图。

        :param args: 可选参数。
        :param kwargs: 可选关键字参数。
        """
        pass

    def update(self, *args, **kwargs):
        """
        更新窗口。

        :param args: 可选参数。
        :param kwargs: 可选关键字参数。
        """
        self.clear_figure()
        self.plot(*args, **kwargs)
        self.draw_canvas()
