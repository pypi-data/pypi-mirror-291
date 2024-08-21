#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_parse_xrdml.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试parse_xrdml.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2024/01/09     create
#       Jiwei Huang        0.0.1         2024/06/11     finish
# ------------------------------------------------------------------
import os
# 导包 =============================================================
import unittest

import numpy as np
import matplotlib.pyplot as plt

from gxusthjw.commons import read_txt
from .parse_xrdml import parse_xrdml, xrdml_to_raw


# ==================================================================
# noinspection DuplicatedCode
class TestParseXrdml(unittest.TestCase):
    """
    测试parse_xrdml.py。
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

    def test_parse_xrdml(self):
        # --------------------------------------------------------
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)
        # --------------------------------------------------------

        test_data_folder = "test_data"
        test_data_folder_path = os.path.join(this_file_path, test_data_folder)
        # --------------------------------------------------------
        xrd_files = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        xrdml_files = ["1.xrdml", "2.xrdml", "3.xrdml", "4.xrdml", "5.xrdml", "6.xrdml"]
        # ---------------------------------------------------------
        xrdml0 = parse_xrdml(os.path.join(test_data_folder_path, xrdml_files[0]))
        xrd0 = read_txt(os.path.join(test_data_folder_path, xrd_files[0]), skiprows=1,
                        res_type="list_numpy")
        plt.plot(xrdml0[0], xrdml0[1], 'b--')
        plt.plot(xrd0[0], xrd0[1] + 1000, 'r-')
        plt.show()
        # ---------------------------------------------------------
        xrdml1 = parse_xrdml(os.path.join(test_data_folder_path, xrdml_files[1]))
        xrd1 = read_txt(os.path.join(test_data_folder_path, xrd_files[1]), skiprows=1,
                        res_type="list_numpy")
        plt.plot(xrdml1[0], xrdml1[1], 'b--')
        plt.plot(xrd1[0], xrd1[1] + 1000, 'r-')
        plt.show()
        # ---------------------------------------------------------
        xrdml2 = parse_xrdml(os.path.join(test_data_folder_path, xrdml_files[2]))
        xrd2 = read_txt(os.path.join(test_data_folder_path, xrd_files[2]), skiprows=1,
                        res_type="list_numpy")
        plt.plot(xrdml2[0], xrdml2[1], 'b--')
        plt.plot(xrd2[0], xrd2[1] + 1000, 'r-')
        plt.show()
        # ---------------------------------------------------------
        xrdml3 = parse_xrdml(os.path.join(test_data_folder_path, xrdml_files[3]))
        xrd3 = read_txt(os.path.join(test_data_folder_path, xrd_files[3]), skiprows=1,
                        res_type="list_numpy")
        plt.plot(xrdml3[0], xrdml3[1], 'b--')
        plt.plot(xrd3[0], xrd3[1] + 1000, 'r-')
        plt.show()
        # ---------------------------------------------------------
        xrdml4 = parse_xrdml(os.path.join(test_data_folder_path, xrdml_files[4]))
        xrd4 = read_txt(os.path.join(test_data_folder_path, xrd_files[4]), skiprows=1,
                        res_type="list_numpy")
        plt.plot(xrdml4[0], xrdml4[1], 'b--')
        plt.plot(xrd4[0], xrd4[1] + 1000, 'r-')
        plt.show()
        # ---------------------------------------------------------
        xrdml5 = parse_xrdml(os.path.join(test_data_folder_path, xrdml_files[5]))
        xrd5 = read_txt(os.path.join(test_data_folder_path, xrd_files[5]), skiprows=1,
                        res_type="list_numpy")
        plt.plot(xrdml5[0], xrdml5[1], 'b--')
        plt.plot(xrd5[0], xrd5[1] + 1000, 'r-')
        plt.show()
        # ---------------------------------------------------------

    def test_xrdml_to_raw(self):
        # --------------------------------------------------------
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)
        # --------------------------------------------------------

        test_data_folder = "test_data"
        test_data_folder_path = os.path.join(this_file_path, test_data_folder)
        # --------------------------------------------------------
        xrd_files = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        xrdml_files = ["1.xrdml", "2.xrdml", "3.xrdml", "4.xrdml", "5.xrdml", "6.xrdml"]
        # ---------------------------------------------------------
        xrdml_to_raw(os.path.join(test_data_folder_path, xrdml_files[0]))


if __name__ == '__main__':
    unittest.main()
