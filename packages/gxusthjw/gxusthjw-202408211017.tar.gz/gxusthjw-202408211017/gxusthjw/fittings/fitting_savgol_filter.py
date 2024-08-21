#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        fitting_savgol_filter.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`基于savgol_filter的平滑器`”的类。
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
import os

from typing import Optional, Union
import numpy as np
import numpy.typing as npt
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from scipy.signal import savgol_filter

from ..commons import unique_string
from . import FittingStatistics
from .fitting_base import FittingBase

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a base class that represents `fitting`.
"""

__all__ = [

]


# 定义 ==============================================================
class SavgolFilterSmoother(FittingBase):
    """
    类`SavgolFilterSmoother`表征“基于savgol_filter的平滑器”。
    """

    def __init__(self, y: npt.ArrayLike,
                 x: Optional[npt.ArrayLike] = None,
                 start: Optional[int] = None,
                 length: Optional[int] = None,
                 method: Optional[Union[str, int]] = None,
                 **kwargs):
        """
        类`SavgolFilterSmoother`的初始化方法。

        :param y: 因变量数据。
        :param x: 自变量数据。
        :param start: 要拟合数据的起始位置索引。
        :param length: 要拟合数据的长度。
        :param method: 拟合方法。
        :param kwargs: 其他可选关键字参数，将全部转化为对象的属性。
        """
        super(SavgolFilterSmoother, self).__init__(y, x, start, length, method, **kwargs)

    def fit(self, **kwargs):
        """
        执行拟合。

        :param kwargs: 拟合所需的关键字参数。
        :return: 拟合结果，拟合统计对象。
        """
        # 关键字参数解析区 ------------------------------------------------
        is_data_out = False
        if hasattr(self, 'is_data_out'):
            is_data_out = self.is_data_out
        data_outfile = None
        if hasattr(self, 'data_outfile'):
            data_outfile = self.data_outfile
        if 'is_data_out' in kwargs and kwargs.pop('is_data_out'):
            is_data_out = True
            data_outfile_name = "LinearFittingSm_" + unique_string()
            if 'data_outfile_name' in kwargs and kwargs['data_outfile_name'] is not None:
                data_outfile_name = kwargs.pop('data_outfile_name')

            data_outpath = os.path.expanduser('~')
            if 'data_outpath' in kwargs and kwargs['data_outpath'] is not None:
                data_outpath = kwargs.pop('data_outpath')

            if not os.path.exists(data_outpath):
                os.makedirs(data_outpath, exist_ok=True)

            data_outfile = os.path.join(data_outpath, "{}.csv".format(data_outfile_name))

        # ------------------------------------------------------------------------------
        is_print_summary = False
        if hasattr(self, 'is_print_summary'):
            is_print_summary = self.is_print_summary
        if 'is_print_summary' in kwargs and kwargs.pop('is_print_summary'):
            is_print_summary = True
        # ------------------------------------------------------------------------------
        is_plot = False
        if hasattr(self, 'is_plot'):
            is_plot = self.is_plot
        is_fig_out = False
        if hasattr(self, 'is_fig_out'):
            is_fig_out = self.is_fig_out
        fig_outfile = None
        if hasattr(self, 'fig_outfile'):
            fig_outfile = self.fig_outfile
        is_show_fig = False
        if hasattr(self, 'is_show_fig'):
            is_show_fig = self.is_show_fig
        if 'is_plot' in kwargs and kwargs.pop('is_plot'):
            is_plot = True
            # 绘图时显示中文。
            plt.rcParams['font.family'] = 'SimHei'
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure(figsize=(8, 6))

        if 'is_fig_out' in kwargs and kwargs.pop('is_fig_out'):
            is_fig_out = True
            fig_outfile_name = "LinearFittingSm_" + unique_string()
            if 'fig_outfile_name' in kwargs and kwargs['fig_outfile_name'] is not None:
                fig_outfile_name = kwargs.pop('fig_outfile_name')

            fig_outpath = os.path.expanduser('~')
            if 'fig_outpath' in kwargs and kwargs['fig_outpath'] is not None:
                fig_outpath = kwargs.pop('fig_outpath')

            if not os.path.exists(fig_outpath):
                os.makedirs(fig_outpath, exist_ok=True)

            fig_outfile = os.path.join(fig_outpath, "{}.png".format(fig_outfile_name))

        if 'is_show_fig' in kwargs:
            is_show_fig = kwargs.pop('is_show_fig')

        # --------------------------------------------------------------
        if 'start' in kwargs:
            start = kwargs.pop('start')
        else:
            start = self.start

        if 'length' in kwargs:
            length = kwargs.pop('length')
        else:
            length = self.length

        # savgol_filter 参数准备 ---------------------------
        if 'window_length' in kwargs:
            if isinstance(kwargs['window_length'], int):
                window_length = kwargs.pop('window_length')
            else:
                raise TypeError('window_length must be int')
        elif hasattr(self, 'window_length'):
            if isinstance(self.window_length, int):
                window_length = self.window_length
            else:
                raise TypeError('window_length must be int')
        else:
            window_length = 201

        if 'polyorder' in kwargs:
            if isinstance(kwargs['polyorder'], int):
                polyorder = kwargs.pop('polyorder')
            else:
                raise TypeError('polyorder must be int')
        elif hasattr(self, 'polyorder'):
            if isinstance(self.polyorder, int):
                polyorder = self.polyorder
            else:
                raise TypeError('polyorder must be int')
        else:
            polyorder = 3

        if 'deriv' in kwargs:
            if isinstance(kwargs['deriv'], int):
                deriv = kwargs.pop('deriv')
            else:
                raise TypeError('deriv must be int')
        elif hasattr(self, 'deriv'):
            if isinstance(self.deriv, int):
                deriv = self.deriv
            else:
                raise TypeError('deriv must be int')
        else:
            deriv = 0

        if 'delta' in kwargs:
            if isinstance(kwargs['delta'], (float, int)):
                delta = kwargs.pop('delta')
            else:
                raise TypeError('delta must be float or int')
        elif hasattr(self, 'delta'):
            if isinstance(self.delta, (float, int)):
                delta = self.delta
            else:
                raise TypeError('delta must be float or int')
        else:
            delta = 1.0

        modes = ('mirror', 'constant', 'nearest', 'wrap', 'interp')
        if 'mode' in kwargs:
            if isinstance(kwargs['mode'], str) and kwargs['mode'].lower() in modes:
                mode = kwargs.pop('mode').lower()
            else:
                raise TypeError("mode must be one of {'mirror', 'constant', 'nearest', 'wrap', 'interp'}.")
        elif hasattr(self, 'mode'):
            if isinstance(self.mode, str) and self.mode.lower() in modes:
                mode = self.mode.lower()
            else:
                raise TypeError("mode must be one of {'mirror', 'constant', 'nearest', 'wrap', 'interp'}.")
        else:
            mode = 'interp'

        if 'cval' in kwargs:
            if isinstance(kwargs['cval'], (float, int)):
                cval = kwargs.pop('cval')
            else:
                raise TypeError('cval must be float or int')
        elif hasattr(self, 'cval'):
            if isinstance(self.cval, (float, int)):
                cval = self.cval
            else:
                raise TypeError('cval must be float or int')
        else:
            cval = 0.0

        p = {'window_length': window_length,
             'polyorder': polyorder,
             'deriv': deriv,
             'delta': delta,
             'mode': mode,
             'cval': cval}

        # 数据准备与拟合 -----------------------------------------------------
        y_var = self.y[start:start + length]
        x_var = self.x[start:start + length]
        if y_var.shape != x_var.shape:
            raise ValueError(f"The shape of the data x[{start}:{start + length}]"
                             f" to be fitted must be the same as of"
                             f"the data y[{start}:{start + length}],"
                             f" but got len(x[{start}:{start + length}])={x_var.shape},"
                             f" and len(y[{start}:{start + length}])={y_var.shape}.")

        res: npt.NDArray = savgol_filter(self.y, **p)
        # noinspection PyTypeChecker
        fs = FittingStatistics(y_var, res, nvars_fitted=3, x=x_var)
        # --------------------------------------------------------------
        # 其他功能区 -----------------------------------------------------
        if is_print_summary:
            print(res)

        if is_data_out:
            assert data_outfile is not None
            data = pd.DataFrame({'x': x_var, 'y': y_var, 'y_fitted': res})
            data.to_csv(data_outfile, index=False)

        if is_show_fig or is_fig_out or is_plot:
            plt.plot(x_var, y_var, label='raw')
            # noinspection PyTypeChecker
            plt.plot(x_var, res, label="fitted")
            plt.legend(loc='best')
            plt.xlabel('x')
            plt.ylabel('y')

            fig_legend_other_text = "x:[{:.2f},{:.2f}]\nwindow_length={:.2f}\npolyorder={:.2f}\nR^2={:.2f}".format(
                min(x_var), max(x_var), window_length, polyorder,
                fs.rsquared)
            ax = plt.gca()
            handles, labels = ax.get_legend_handles_labels()
            handles.append(mpatches.Patch(color='none', label=fig_legend_other_text))
            plt.rc('legend', fontsize=16)
            plt.legend(loc='best', handles=handles)

        if is_fig_out:
            assert fig_outfile is not None
            plt.savefig(fig_outfile)

        if is_show_fig:
            plt.show()
        # --------------------------------------------------------------
        return res, fs

    def interactive_fit(self, **kwargs):
        """
        交互式执行拟合。

        :param kwargs: 拟合所需的关键字参数。
        :return: 拟合结果，拟合统计对象。
        """
        pass
