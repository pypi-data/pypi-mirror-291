#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        parse_xrdml.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 用于解析.xrdml格式的数据。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/07/12     revise
#       Jiwei Huang        0.0.1         2024/08/19     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
import os
import xml.dom.minidom
from typing import Optional, Tuple

import numpy as np
import numpy.typing as npt

# 定义 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Processing xrd data file with .xrdml format.
"""

__all__ = [
    'parse_xrdml',
    'xrdml_to_raw'
]


# ==================================================================

def parse_xrdml(xrdml_file: str) -> Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """
    解析.xrdml格式的XRD数据文件。

    :param xrdml_file: .xrdml格式的XRD数据文件的完整路径。
    :return theta2_data, intensity_data
    """
    dom = xml.dom.minidom.parse(xrdml_file)
    root = dom.documentElement
    data = root.getElementsByTagName('positions')

    theta2_start = 0
    theta2_end = 1

    for i in data:
        # print(i.getAttribute('axis'))
        if i.getAttribute('axis') == "2Theta":
            theta2 = i.getElementsByTagName("startPosition")
            theta2_start = theta2[0].firstChild.data
            theta2_start = float(theta2_start)
            theta2 = i.getElementsByTagName("endPosition")
            theta2_end = theta2[0].firstChild.data
            theta2_end = float(theta2_end)

    intensity = root.getElementsByTagName('intensities')
    intensity_str = intensity[0].firstChild.data
    intensity_str_data = intensity_str.split()

    n = len(intensity_str_data)
    theta2_data = np.linspace(theta2_start, theta2_end, n, dtype=np.float64)
    intensity_data = np.array([int(s) for s in intensity_str_data], dtype=np.int32)
    return theta2_data, intensity_data


# noinspection PyTypeChecker,DuplicatedCode
def xrdml_to_raw(xrdml_file: str,
                 theta2_round: Optional[int] = 6,
                 separator: Optional[str] = None) -> None:
    """
    解析.xrdml格式的XRD数据文件，并将其保存为.raw或.txt格式的文件。

    :param xrdml_file: .xrdml格式的XRD数据文件的完整路径。
    :param theta2_round: theta2保留的数据位数，若为None,则不进行四舍五入运算。
    :param separator: 保存文件的分隔符，若为None,则以“\t”为分隔符，保存文件后缀名为.raw,
                      若不为None,则以指定分隔符为分隔符，保存文件后缀名为.txt。
    """
    theta2_data, intensity_data = parse_xrdml(xrdml_file)
    data_length = len(theta2_data)
    # 使用 split() 分离路径和文件名
    path, filename = os.path.split(xrdml_file)

    # 使用 splitext() 分离文件名和扩展名
    basename, extension = os.path.splitext(filename)

    if separator is None:
        separator = "\t"
        outfile = os.path.join(path, basename + ".raw")
        print(outfile)
        if theta2_round is not None:
            with open(outfile, "w") as file:
                for i in range(data_length):
                    file.write(str(round(theta2_data[i], theta2_round)) + separator + str(intensity_data[i]) + "\n")
        else:
            with open(outfile, "w") as file:
                for i in range(data_length):
                    file.write(str(theta2_data[i]) + separator + str(intensity_data[i]) + "\n")
    else:
        outfile = os.path.join(path, basename + ".txt")
        if theta2_round is not None:
            with open(outfile, "w") as file:
                for i in range(data_length):
                    file.write(str(round(theta2_data[i], theta2_round)) + separator + str(intensity_data[i]) + "\n")
        else:
            with open(outfile, "w") as file:
                for i in range(data_length):
                    file.write(str(theta2_data[i]) + separator + str(intensity_data[i]) + "\n")
    print("All done!")
