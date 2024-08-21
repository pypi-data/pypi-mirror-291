#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        dataframe_view.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“标准`DataFrame视图`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 ============================================================
import pandas as pd
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTableView

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents a `DataFrame view`.
"""

__all__ = [
    'DataFrameView'
]


# 定义 ============================================================

class DataFrameView(QTableView):
    """
    类`DataFrameView`表征“DataFrame视图”。
    """

    def __init__(self, parent=None):
        """
        类`DataFrameView`的初始化方法。

        :param parent: 父控件。
        """
        super().__init__(parent)

    def set_dataframe(self, df: pd.DataFrame):
        """
        设置要呈现的DataFrame对象。

        :param df: 要呈现的DataFrame对象。
        """
        model = QStandardItemModel(df.shape[0], df.shape[1], self)
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                model.setItem(row, col, QStandardItem(str(df.iat[row, col])))
        model.setHorizontalHeaderLabels(df.columns)
        self.setModel(model)
