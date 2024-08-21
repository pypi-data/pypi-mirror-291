#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_typing_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试typing_utils.py。
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
# 导包 =============================================================
import unittest
import numpy as np
from .typing_utils import is_numericarraylike


# ==================================================================
class TestTypingUtils(unittest.TestCase):
    """
    测试typing_utils.py。
    """

    # --------------------------------------------------------------------
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

    # --------------------------------------------------------------------

    def test_numericarraylike(self):
        test_cases = [
            np.array([1, 2, 3]),
            [1, 2, 3],
            [1.0, 2.0, 3.0],
            "123",
            [1, 2, "3"],
            np.array([1, 2, 3], dtype=object),
            (1, 2, 3),
            {1, 2, 3},
        ]

        for case in test_cases:
            print(f"{case}: {is_numericarraylike(case)}")

        # 示例用法
        print(is_numericarraylike(np.array([1, 2, 3])))  # 输出: True
        print(is_numericarraylike([1, 2, 3]))  # 输出: True
        print(is_numericarraylike([1.0, 2.0, 3.0]))  # 输出: True
        print(is_numericarraylike("123"))  # 输出: False
        print(is_numericarraylike([1, 2, "3"]))  # 输出: False


if __name__ == '__main__':
    unittest.main()
