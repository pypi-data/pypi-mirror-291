#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        linear_fitting.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 承载“线性拟合”相关的函数和类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxx() -- xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/15     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import os
from enum import Enum, auto
from typing import Optional, Union
import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statsmodels.api as sm
from matplotlib.widgets import Slider, RadioButtons, Button

from .fitting_statistics import FittingStatistics
from .fitting_base import FittingBase

from ..commons import unique_string

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Assembling classes and functions associated with `linear fitting`.
"""

__all__ = [
    'LinearFittingMethodSm',
    'LinearFittingSm',
    'linear_fitting_sm_rlm',
    'linear_fitting_sm_ols',
    'linear_fitting_sm',
    'interactive_linear_fitting_sm'
]


# ==================================================================

# 基于statsmodels的线性拟合 ------------------------------------------
class LinearFittingMethodSm(Enum):
    """
    枚举类`LinearFittingMethodSm`表征“基于statsmodels模块的线性拟合方法”。
    """

    RLM = auto()
    """
    Robust Linear Model
    """

    OLS = auto()
    """
    Ordinary Least Squares
    """

    @staticmethod
    def of(value: Union[int, str]):
        """
        从值或成员名（忽略大小写）构建枚举实例。

        :param value: 指定的值或成员名（忽略大小写）。
        :return: LinearFittingMethodSm对象。
        :rtype: LinearFittingMethodSm
        """
        if isinstance(value, str):
            if value.upper() in LinearFittingMethodSm.__members__:
                return LinearFittingMethodSm.__members__[value]
            else:
                raise ValueError(f"Unknown value ({value}) for LinearFittingMethodSm.")
        elif isinstance(value, int):
            for member in LinearFittingMethodSm:
                if member.value == value:
                    return member
            raise ValueError(f"Unknown value ({value}) for LinearFittingMethodSm.")
        else:
            raise ValueError(f"Unknown value ({value}) for LinearFittingMethodSm.")


class LinearFittingSm(FittingBase):
    """
    类`LinearFittingSm`表征“基于statsmodels（OLS或RLM）的线性拟合”
    """

    def __init__(self, y: npt.ArrayLike,
                 x: Optional[npt.ArrayLike] = None,
                 start: Optional[int] = None,
                 length: Optional[int] = None,
                 method: Union[str, int, LinearFittingMethodSm] = "ols",
                 **kwargs):
        """
        类`LinearFittingSm`的初始化方法。

        :param y: 因变量数据。
        :param x: 自变量数据。
        :param start: 要拟合数据的起始位置索引。
        :param length: 要拟合数据的长度。
        :param method: 拟合方法。
        :param kwargs: 其他可选关键字参数，将全部转化为对象的属性。
        """
        # 解析method
        if method is None:
            method = "ols"
        else:
            if isinstance(method, LinearFittingMethodSm):
                method = method.name.lower()
            elif isinstance(method, (int, str)):
                method = LinearFittingMethodSm.of(method).name.lower()
            else:
                raise ValueError(f"Unknown value ({method}) for LinearFittingSm.")
        super(LinearFittingSm, self).__init__(y, x, start, length, method, **kwargs)

    # noinspection DuplicatedCode
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

        if 'method' in kwargs:
            method = kwargs.pop('method')
        else:
            method = self.method
        # 数据准备与拟合 -----------------------------------------------------
        y_var = self.y[start:start + length]
        x_var = self.x[start:start + length]
        if y_var.shape != x_var.shape:
            raise ValueError(f"The shape of the data x[{start}:{start + length}]"
                             f" to be fitted must be the same as of"
                             f"the data y[{start}:{start + length}],"
                             f" but got len(x[{start}:{start + length}])={x_var.shape},"
                             f" and len(y[{start}:{start + length}])={y_var.shape}.")
        x_var_ff = np.column_stack((x_var,))
        x_var_ff = sm.add_constant(x_var_ff)
        if method.lower() == 'ols':
            fitting_res = sm.OLS(y_var, x_var_ff).fit()
        elif method.lower() == 'rlm':
            fitting_res = sm.RLM(y_var, x_var_ff).fit()
        else:
            raise ValueError(f"Method {method} not supported.")

        # noinspection PyTypeChecker
        fs = FittingStatistics(y_var, fitting_res.fittedvalues, nvars_fitted=2, x=x_var)
        # --------------------------------------------------------------
        # 其他功能区 -----------------------------------------------------
        if is_print_summary:
            print(fitting_res.summary())

        if is_data_out:
            assert data_outfile is not None
            data = pd.DataFrame({'x': x_var, 'y': y_var, 'y_fitted': fitting_res.fittedvalues})
            data.to_csv(data_outfile, index=False)

        if is_show_fig or is_fig_out or is_plot:
            plt.plot(x_var, y_var, label='raw')
            # noinspection PyTypeChecker
            plt.plot(x_var, fitting_res.fittedvalues, label="fitted")
            plt.legend(loc='best')
            plt.xlabel('x')
            plt.ylabel('y')

            fig_legend_other_text = "x:[{:.2f},{:.2f}]\nSlope={:.2f}\nIntercept={:.2f}\nR^2={:.2f}".format(
                min(x_var), max(x_var), fitting_res.params[0], fitting_res.params[1],
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
        return fitting_res, fs

    def interactive_fit(self, **kwargs):
        """
        交互式执行拟合。

        :param kwargs: 拟合所需的关键字参数。
        :return: 拟合后的因变量数据，拟合统计对象。
        """
        return interactive_linear_fitting_sm(self.y, self.x)


# noinspection PyTypeChecker
def linear_fitting_sm_rlm(y: npt.NDArray,
                          x: npt.NDArray):
    """
    基于statsmodels提供的线性拟合方法（RLM）对指定的数据（y，x）执行拟合。

    要求：

        1. y为一维数值数组。

        2. x为一维数值数组。

        3. y的长度与x的长度相同，但本方法不做长度相等性检查。

    :param y: 因变量。
    :param x: 自变量。
    :return: 拟合结果。
    """
    x_var = np.column_stack((x,))
    x_var = sm.add_constant(x_var)
    fitting_res = sm.RLM(y, x_var).fit()
    return fitting_res, FittingStatistics(y, fitting_res.fittedvalues, nvars_fitted=2, x=x)


# noinspection PyTypeChecker
def linear_fitting_sm_ols(y: npt.NDArray,
                          x: npt.NDArray):
    """
    基于statsmodels提供的线性拟合方法（OLS）对指定的数据（y，x）执行拟合。

    要求：

        1. y为一维数值数组。

        2. x为一维数值数组。

        3. y的长度与x的长度相同，但本方法不做长度相等性检查。

    :param y: 因变量。
    :param x: 自变量。
    :return: 拟合结果。
    """
    x_var = np.column_stack((x,))
    x_var = sm.add_constant(x_var)
    fitting_res = sm.OLS(y, x_var).fit()
    return fitting_res, FittingStatistics(y, fitting_res.fittedvalues, nvars_fitted=2, x=x)


# noinspection DuplicatedCode,PyTypeChecker
def linear_fitting_sm(y: npt.ArrayLike,
                      x: Optional[npt.ArrayLike] = None,
                      start: Optional[int] = None,
                      length: Optional[int] = None,
                      method: Union[str, LinearFittingMethodSm] = "ols",
                      **kwargs):
    """
    基于statsmodels提供的线性拟合方法（OLS或RLM）对指定的数据（y，x）执行拟合。

    :param y: 因变量。
    :param x: 自变量。
    :param start: 要拟合数据的起始位置索引。
    :param length: 要拟合数据的长度。
    :param method: 拟合方法（OLS或RLM）。
    :param kwargs: 其他可选关键字参数。
    :return: 拟合结果。
    """
    # 关键字参数解析区 ------------------------------------------------
    is_data_out = False
    data_outfile = None
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
    if 'is_print_summary' in kwargs and kwargs.pop('is_print_summary'):
        is_print_summary = True
    # ------------------------------------------------------------------------------
    is_plot = False
    is_fig_out = False
    fig_outfile = None
    is_show_fig = False
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

    # 位置参数解析区 --------------------------------------------------
    ys = np.asarray(y)
    ys_len = ys.shape[0]

    if x is None:
        xs = np.arange(ys_len, dtype=np.int64)
    else:
        xs = np.asarray(x)
    xs_len = xs.shape[0]

    if start is None:
        start = 0
    if length is None:
        length = xs_len if ys_len >= xs_len else ys_len

    # --------------------------------------------------------------

    # 数据准备与拟合 -----------------------------------------------------
    y_var = ys[start:start + length]
    x_var = xs[start:start + length]
    if y_var.shape != x_var.shape:
        raise ValueError(f"The shape of the data x[{start}:{start + length}]"
                         f" to be fitted must be the same as of"
                         f"the data y[{start}:{start + length}],"
                         f" but got len(x[{start}:{start + length}])={x_var.shape},"
                         f" and len(y[{start}:{start + length}])={y_var.shape}.")
    x_var_ff = np.column_stack((x_var,))
    x_var_ff = sm.add_constant(x_var_ff)
    if isinstance(method, LinearFittingMethodSm):
        if method == LinearFittingMethodSm.OLS:
            fitting_res = sm.OLS(y_var, x_var_ff).fit()
        elif method == LinearFittingMethodSm.RLM:
            fitting_res = sm.RLM(y_var, x_var_ff).fit()
        else:
            raise ValueError(f"Method {method} not supported.")
    elif isinstance(method, str):
        if method.lower() == 'ols':
            fitting_res = sm.OLS(y_var, x_var_ff).fit()
        elif method.lower() == 'rlm':
            fitting_res = sm.RLM(y_var, x_var_ff).fit()
        else:
            raise ValueError(f"Method {method} not supported.")
    else:
        raise ValueError(f"Method {method} not supported.")

    fs = FittingStatistics(y_var, fitting_res.fittedvalues, nvars_fitted=2, x=x_var)
    # --------------------------------------------------------------

    # 其他功能区 -----------------------------------------------------
    if is_print_summary:
        print(fitting_res.summary())

    if is_data_out:
        assert data_outfile is not None
        data = pd.DataFrame({'x': x_var, 'y': y_var, 'y_fitted': fitting_res.fittedvalues})
        data.to_csv(data_outfile, index=False)

    if is_show_fig or is_fig_out or is_plot:
        plt.plot(x_var, y_var, label='raw')
        plt.plot(x_var, fitting_res.fittedvalues, label="fitted")
        plt.legend(loc='best')
        plt.xlabel('x')
        plt.ylabel('y')

        fig_legend_other_text = "x:[{:.2f},{:.2f}]\nSlope={:.2f}\nIntercept={:.2f}\nR^2={:.2f}".format(
            min(x_var), max(x_var), fitting_res.params[0], fitting_res.params[1],
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
    return fitting_res


# noinspection DuplicatedCode
def _linear_fitting_sm(ys: npt.NDArray,
                       xs: npt.NDArray,
                       start: int,
                       length: int,
                       method: str):
    """
    基于statsmodels提供的线性拟合方法（OLS或RLM）对指定的数据（y，x）执行拟合。

    此函数主要是为`interactive_linear_fitting_sm`函数服务。

    :param ys: 因变量。
    :param xs: 自变量。
    :param start: 要拟合数据的起始位置索引。
    :param length: 要拟合数据的长度。
    :param method: 拟合方法（OLS或RLM）。
    :return: 拟合结果。
    """
    y_var = ys[start:start + length]
    x_var = xs[start:start + length]
    if y_var.shape != x_var.shape:
        raise ValueError(f"The shape of the data x[{start}:{start + length}]"
                         f" to be fitted must be the same as of"
                         f"the data y[{start}:{start + length}],"
                         f" but got len(x[{start}:{start + length}])={x_var.shape},"
                         f" and len(y[{start}:{start + length}])={y_var.shape}.")
    x_var_ff = np.column_stack((x_var,))
    x_var_ff = sm.add_constant(x_var_ff)
    if isinstance(method, LinearFittingMethodSm):
        if method == LinearFittingMethodSm.OLS:
            fitting_res = sm.OLS(y_var, x_var_ff).fit()
        elif method == LinearFittingMethodSm.RLM:
            fitting_res = sm.RLM(y_var, x_var_ff).fit()
        else:
            raise ValueError(f"Method {method} not supported.")
    elif isinstance(method, str):
        if method.lower() == 'ols':
            fitting_res = sm.OLS(y_var, x_var_ff).fit()
        elif method.lower() == 'rlm':
            fitting_res = sm.RLM(y_var, x_var_ff).fit()
        else:
            raise ValueError(f"Method {method} not supported.")
    else:
        raise ValueError(f"Method {method} not supported.")

    return fitting_res, x_var, y_var


# noinspection DuplicatedCode
def interactive_linear_fitting_sm(y: npt.ArrayLike,
                                  x: Optional[npt.ArrayLike] = None):
    """
    基于statsmodels提供的线性拟合方法（OLS或RLM）,
    交互式地对指定的数据（y，x）执行拟合。

    :param y: 因变量。
    :param x: 自变量。
    :return: 拟合结果，拟合统计
    """
    # ------------------------------------------------------------
    ys = np.asarray(y)
    ys_len = ys.shape[0]

    if x is None:
        xs = np.arange(ys_len, dtype=np.int64)
    else:
        xs = np.asarray(x)
    xs_len = xs.shape[0]

    start = 0
    length = xs_len if ys_len >= xs_len else ys_len
    # ------------------------------------------------------------

    method_selected = 'OLS'
    start_selected = start
    length_selected = length
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    fitting_res = None
    x_var = None
    y_var = None
    fs = None

    # ------------------------------------------------------------
    # noinspection DuplicatedCode,PyTypeChecker
    def update():
        nonlocal ax
        nonlocal start_selected
        nonlocal length_selected
        nonlocal method_selected
        nonlocal fitting_res
        nonlocal x_var
        nonlocal y_var
        nonlocal fs

        ax.cla()

        fitting_res, x_var, y_var = _linear_fitting_sm(
            ys, xs,
            start_selected,
            length_selected,
            method_selected
        )
        fs = FittingStatistics(y_var, fitting_res.fittedvalues, nvars_fitted=2, x=x_var)
        ax.plot(x_var, y_var, label='raw')
        ax.plot(x_var, fitting_res.fittedvalues, label='fitted')
        plt.xlabel('x')
        plt.ylabel('y')
        fig_legend_other_text = "x:[{:.2f},{:.2f}]\nSlope={:.2f}\nIntercept={:.2f}\nR^2={:.2f}".format(
            min(x_var), max(x_var), fitting_res.params[0], fitting_res.params[1],
            fs.rsquared)

        handles, labels = ax.get_legend_handles_labels()
        handles.append(mpatches.Patch(color='none', label=fig_legend_other_text))
        plt.rc('legend', fontsize=10)
        ax.legend(loc='best', handles=handles)

    update()

    methods = ['OLS', 'RLM']
    radio_ax = plt.axes((0.78, 0.02, 0.1, 0.09))
    radio = RadioButtons(radio_ax, methods, active=0)

    # 添加一个滑块
    start_slider_ax = plt.axes((0.1, 0.08, 0.6, 0.03))
    start_slider = Slider(start_slider_ax, 'Start', 0, len(y) - 3, valinit=start)

    # 添加一个滑块
    length_slider_ax = plt.axes((0.1, 0.02, 0.6, 0.03))
    length_slider = Slider(length_slider_ax, 'Length', 0, len(y), valinit=length)

    save_button_ax = plt.axes((0.9, 0.02, 0.08, 0.09))
    save_button = Button(save_button_ax, 'Save')

    # 当选项改变时的回调函数
    # noinspection PyShadowingNames,DuplicatedCode
    def change_option(label):
        nonlocal method_selected
        method_selected = label
        update()

    # 设置选项改变时调用的函数
    radio.on_clicked(change_option)

    # 滑块数值变化事件处理函数
    # noinspection PyShadowingNames,DuplicatedCode
    def on_start_slider_change(val):
        nonlocal start_selected
        start_selected = int(val)
        update()

    start_slider.on_changed(on_start_slider_change)

    # 滑块数值变化事件处理函数
    # noinspection PyShadowingNames,DuplicatedCode
    def on_length_slider_change(val):
        nonlocal length_selected
        length_selected = int(val)
        update()

    length_slider.on_changed(on_length_slider_change)

    # noinspection PyUnusedLocal,PyUnresolvedReferences
    def on_save_button_change(val):
        nonlocal ys
        nonlocal xs
        nonlocal start_selected
        nonlocal length_selected
        nonlocal method_selected
        nonlocal fitting_res
        data_file_path = os.getcwd()
        data_file_name = "LinearFittingSm_" + unique_string() + ".csv"
        data_outfile = os.path.join(data_file_path, data_file_name)
        data = pd.DataFrame({'x': x_var, 'y': y_var, 'y_fitted': fitting_res.fittedvalues})
        data.to_csv(data_outfile, index=False)

    save_button.on_clicked(on_save_button_change)

    plt.show()

    return fitting_res, fs
# ------------------------------------------------------------------
