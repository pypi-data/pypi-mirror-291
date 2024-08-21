#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_str_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试str_utils.py。
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

from .str_utils import str_partition


# ==================================================================
class TestStrUtils(unittest.TestCase):
    """
    测试str_utils.py。
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

    # ===================================================================
    def test_str_partition(self):
        """
        测试str_partition(s: str, delimiter: str)方法。
        """
        s1 = "js1h1-2 1.1cm(1)"
        s2 = "3h1-2 10mm"
        s3 = "3h1-2 10mm 3h1-2 10mm"
        s4 = "js1h1-2 1.1cm(1) js1h1-2 1.1cm(1)"
        s5 = "3h1-3 10mm"
        s6 = "3h1-3 10mm -2"
        print(str_partition(s1, '-2'))
        print(str_partition(s2, '-2'))
        print(str_partition(s3, '-2'))
        print(str_partition(s4, '-2'))
        print(str_partition(s5, '-2'))
        print(str_partition(s6, '-2'))
        self.assertEqual(str_partition(s1, '-2'), ("js1h1-2", " 1.1cm(1)"))
        self.assertEqual(str_partition(s2, '-2'), ("3h1-2", " 10mm"))
        self.assertEqual(str_partition(s3, '-2'), ("3h1-2", " 10mm 3h1-2 10mm"))
        self.assertEqual(str_partition(s4, '-2'), ("js1h1-2", " 1.1cm(1) js1h1-2 1.1cm(1)"))
        self.assertEqual(str_partition(s5, '-2'), ("3h1-3 10mm", ""))
        self.assertEqual(str_partition(s6, '-2'), ("3h1-3 10mm -2", ""))


if __name__ == '__main__':
    unittest.main()
