#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        about_window.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2024/08/15
# Description:      Main Function: 定义“表征`关于窗口`”的类。
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
from .window_base import WindowBase

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `about window`.
"""

__all__ = [
    "AboutWindow"
]


# 定义 ================================================================


class AboutWindow(WindowBase):
    """
    类`AboutWindow`表征“关于窗口”。
    """

    def __init__(self, master, about_text, **kwargs):
        """
        类`AboutWindow`的初始化方法。

        Args:
            master (tk.Tk): The master window.
        """
        super().__init__(master, **kwargs)

        # Add some content to the about window
        label = tk.Label(self.top, text=about_text)
        label.pack(padx=20, pady=20)

        # Close button
        button_close = tk.Button(self.top, text="Close", command=self.close)
        button_close.pack(pady=10)

