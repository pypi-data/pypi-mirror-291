#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_experimental_data.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试experimental_data.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/18     finish
# -----------------------------------------------------------------
# 导包 =============================================================
import unittest

from .experimental_data import ExperimentalData


# 定义 =============================================================

class TestExperimentalData(unittest.TestCase):
    """
    测试experimental_data.py。
    """

    # ==============================================================
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

    # ==============================================================

    # noinspection DuplicatedCode,PyUnresolvedReferences
    def test_init(self):
        td = ExperimentalData()
        self.assertEqual('specimen', td.specimen_name)
        self.assertEqual(0, td.specimen_no)
        self.assertEqual('specimen_0', td.sample_name)

        td1 = ExperimentalData(specimen_name='a')
        self.assertEqual('a', td1.specimen_name)
        self.assertEqual(0, td1.specimen_no)
        self.assertEqual('a_0', td1.sample_name)

        td2 = ExperimentalData(specimen_no=2)
        self.assertEqual('specimen', td2.specimen_name)
        self.assertEqual(2, td2.specimen_no)
        self.assertEqual('specimen_2', td2.sample_name)

        td3 = ExperimentalData(specimen_name='c', specimen_no=5)
        self.assertEqual('c', td3.specimen_name)
        self.assertEqual(5, td3.specimen_no)
        self.assertEqual('c_5', td3.sample_name)

        td4 = ExperimentalData(aa=10)
        self.assertEqual(10, td4.aa)
        self.assertEqual('specimen', td4.specimen_name)
        self.assertEqual(0, td4.specimen_no)
        self.assertEqual('specimen_0', td4.sample_name)

        td5 = ExperimentalData(specimen_name='a', aa=10)
        self.assertEqual(10, td5.aa)
        self.assertEqual('a', td5.specimen_name)
        self.assertEqual(0, td5.specimen_no)
        self.assertEqual('a_0', td5.sample_name)

        td6 = ExperimentalData(specimen_no=2, aa=10)
        self.assertEqual(10, td6.aa)
        self.assertEqual('specimen', td6.specimen_name)
        self.assertEqual(2, td6.specimen_no)
        self.assertEqual('specimen_2', td6.sample_name)

        td7 = ExperimentalData(specimen_name='c', specimen_no=5, aa=10)
        self.assertEqual(10, td7.aa)
        self.assertEqual('c', td7.specimen_name)
        self.assertEqual(5, td7.specimen_no)
        self.assertEqual('c_5', td7.sample_name)


if __name__ == '__main__':
    unittest.main()
