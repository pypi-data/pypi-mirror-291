#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        settings_window.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2024/08/15
# Description:      Main Function: 定义“表征`设置窗口`”的类。
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
from .about_window import AboutWindow
from .window_base import WindowBase

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `settings window`.
"""

__all__ = ["SettingsWindow"]


# 定义 ================================================================
class SettingsWindow(WindowBase):
    """
    类`SettingsWindow`表征“设置窗口”。
    """

    # noinspection PyUnresolvedReferences
    def __init__(self, master, **kwargs):
        """
        类`SettingsWindow`的初始化方法。

        :param master: 主窗口，(tk.Tk)。
        :param kwargs:其他关键字参数，将被转化为对象的属性。
        """
        super(SettingsWindow, self).__init__(master, **kwargs)
        # -------------------------------------------------------------
        # Create a menu bar
        self.menubar = tk.Menu(self.top)
        self.top.config(menu=menubar)

        # Create a file menu
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        # Create a help menu
        self.help_menu = tk.Menu(menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about_window)

        # Add the menus to the menu bar
        self.menubar.add_cascade(label="File", menu=file_menu)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        # -------------------------------------------------------------

    def show_about_window(self):
        """
        Show the about window.
        """
        txt = """
        Copyright © 2024 Jiwei Huang [huangjiwei@gxust.edu.cn]
        
        This program is free software: you can redistribute it and/or modify it
         under the terms of the MIT License.
        """
        AboutWindow(self.master, about_text=txt)
