#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_path_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试path_utils.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/01/01     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import os.path
import unittest
from .path_utils import (join_file_path, sep_file_path,
                         print_files_and_folders,
                         print_top_level_files_and_folders,
                         list_top_level_files_and_folders)


# ==================================================================
class TestPathUtils(unittest.TestCase):
    """
    测试path_utils.py。
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

    def test_join_file_path(self):
        path = "c:/a"
        file_name = "b"
        file_type = ".pdf"
        print(join_file_path(path, file_name, file_type))
        self.assertEqual('c:/a\\b.pdf', join_file_path(path, file_name, file_type))
        file_type = "pdf"
        print(join_file_path(path, file_name, file_type))
        self.assertEqual('c:/a\\b.pdf', join_file_path(path, file_name, file_type))

        file_type = " pdf "
        print(join_file_path(path, file_name, file_type))
        self.assertEqual('c:/a\\b.pdf', join_file_path(path, file_name, file_type))

    def test_sep_file_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test_folder = "test_data"
        path = os.path.join(path, test_folder)
        file_name = "b"
        file_type = ".pdf"
        print(join_file_path(path, file_name, file_type))
        print(sep_file_path(join_file_path(path, file_name, file_type),
                            with_dot_in_ext=False))

        path = 'c:/a\\b.pdf'
        file_path, file_name, file_ext = sep_file_path(path)
        print(file_path)
        print(file_name)
        print(file_ext)
        self.assertEqual("c:/a", file_path)
        self.assertEqual("b", file_name)
        self.assertEqual(".pdf", file_ext)

    def test_list_files_and_folders(self):
        path = r'I:\Projects\Aliyun\huangjiwei\gxusthjw-workbench\Python\gxusthjw-python'
        print_files_and_folders(path)

    def test_print_top_level_files_and_folders(self):
        path = r'I:\Projects\Aliyun\huangjiwei\gxusthjw-workbench\Python\gxusthjw-python'
        print_top_level_files_and_folders(path)

    def test_list_top_level_files_and_folders(self):
        path = r'I:\Projects\Aliyun\huangjiwei\gxusthjw-workbench\Python\gxusthjw-python'
        folders, files = list_top_level_files_and_folders(path)
        for folder in folders:
            print(folder)
        for file in files:
            print(file)


if __name__ == '__main__':
    unittest.main()
