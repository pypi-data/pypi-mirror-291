#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_monotonic_functions.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试monotonic_functions.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/15     revise
#       Jiwei Huang        0.0.1         2026/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import unittest
import numpy as np
import matplotlib.pyplot as plt
from .monotonic_functions import (monotonic_power,
                                  monotonic_linear,
                                  monotonic_log)


# ==================================================================
class TestMonotonicFunctions(unittest.TestCase):
    """
    测试monotonic_functions。
    """

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        print("\n\n-----------------------------------------------------")

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        print("-----------------------------------------------------")

    @classmethod
    def setUpClass(cls):
        """
        Hook method for setting up class fixture before running tests in the class.
        """
        print("\n\n=======================================================")

    @classmethod
    def tearDownClass(cls):
        """
        Hook method for deconstructing the class fixture after running all tests in the class.
        """
        print("=======================================================")

    def test_monotonic_linear(self):
        x = np.linspace(-100, 100, 10000)
        y1 = monotonic_linear(x, 3, 5)
        y2 = monotonic_linear(x, -3, 5)
        plt.plot(x, y1, label="a=3,b=5")
        plt.plot(x, y2, label="a=-3,b=5")
        plt.legend(loc="best")
        plt.show()

    def test_monotonic_log(self):
        x = np.linspace(1, 5, 1000)
        print(x)
        y1 = monotonic_log(x, 3, 5, -10)
        print(y1)
        y2 = monotonic_log(x, 0.3, 5, -10)
        print(y2)
        plt.plot(x, y1, label="a=3,b=5,c=10")
        plt.legend(loc="best")
        plt.show()
        plt.plot(x, y2, label="a=0.3,b=5,c=10")
        plt.legend(loc="best")
        plt.show()

    def test_monotonic_power(self):
        x = np.linspace(-100, 100, 10000)
        y1 = monotonic_power(x, 3, 5, 10)
        y2 = monotonic_power(x, -3, 5, 10)
        plt.plot(x, y1, label="a=3,b=5")
        plt.plot(x, y2, label="a=-3,b=5")
        plt.legend(loc="best")
        plt.show()


if __name__ == '__main__':
    unittest.main()
