#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        exceptions.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“自定义异常类”。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/05/30     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/08/04     revise
# ----------------------------------------------------------------
# 导包 ============================================================

# 声明 ============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Defining custom exception classes.
"""
__all__ = [
    'ExceptionBase',
    'StateException',
]


# 定义 ==============================================================

class ExceptionBase(Exception):
    def __init__(self, message, *args):
        self.message = message
        super(ExceptionBase, self).__init__(self.message, *args)


class StateException(ExceptionBase):
    def __init__(self, message, *args):
        super(StateException, self).__init__(message, *args)
