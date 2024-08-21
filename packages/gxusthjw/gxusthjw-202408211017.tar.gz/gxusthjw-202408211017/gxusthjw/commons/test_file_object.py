#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_file_object.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试file_object.py。
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
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     finish
# ------------------------------------------------------------------
# 导包 =============================================================
import os
import unittest

from .file_object import (get_file_encoding_chardet,
                          file_info,
                          get_file_info,
                          get_file_info_of_module,
                          FileInfo,
                          FileObject)


# ==================================================================
# noinspection DuplicatedCode,PyUnresolvedReferences
class TestFileObject(unittest.TestCase):
    """
    测试file_object.py。
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
    def test_get_file_encoding_chardet(self):
        """
        测试`get_file_encoding_chardet`方法。
        """
        # --------------------------------------------------------------
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)

        test_data_folder = "test_data/file_object"
        test_data_path = os.path.join(this_file_path, test_data_folder)
        # --------------------------------------------------------------
        gkb_file = os.path.join(test_data_path, "ansi_file.txt")
        gkb_file_encoding = get_file_encoding_chardet(gkb_file)
        print("gkb_file_encoding(type({})):{}".format(type(gkb_file_encoding),
                                                      gkb_file_encoding))
        self.assertEqual(gkb_file_encoding, "ascii")

        gkb_file = os.path.join(test_data_path, "GB2312_file.txt")
        gkb_file_encoding = get_file_encoding_chardet(gkb_file)
        print("gkb_file_encoding(type({})):{}".format(type(gkb_file_encoding),
                                                      gkb_file_encoding))
        self.assertEqual(gkb_file_encoding, "IBM855")

        gkb_file = os.path.join(test_data_path, "gkb_file.txt")
        gkb_file_encoding = get_file_encoding_chardet(gkb_file)
        print("gkb_file_encoding(type({})):{}".format(type(gkb_file_encoding),
                                                      gkb_file_encoding))
        self.assertEqual(gkb_file_encoding, "GB2312")

        utf8_file = os.path.join(test_data_path, "utf8_file.txt")
        utf8_file_encoding = get_file_encoding_chardet(utf8_file)
        print("utf8_file_encoding(type({})):{}".format(type(utf8_file_encoding),
                                                       utf8_file_encoding))
        self.assertEqual(utf8_file_encoding, "utf-8")

        utf16_file = os.path.join(test_data_path, "utf16_file.txt")
        utf16_file_encoding = get_file_encoding_chardet(utf16_file)
        print("utf16_file_encoding(type({})):{}".format(type(utf16_file_encoding),
                                                        utf16_file_encoding))
        self.assertEqual(utf16_file_encoding, "UTF-16")

        utf16be_file = os.path.join(test_data_path, "utf16be_file.txt")
        utf16be_file_encoding = get_file_encoding_chardet(utf16be_file)
        print("utf16be_file_encoding(type({})):{}".format(type(utf16be_file_encoding),
                                                          utf16be_file_encoding))
        self.assertEqual(utf16be_file_encoding, "UTF-16")

        utf16le_file = os.path.join(test_data_path, "utf16le_file.txt")
        utf16le_file_encoding = get_file_encoding_chardet(utf16le_file)
        print("utf16le_file_encoding(type({})):{}".format(type(utf16le_file_encoding),
                                                          utf16le_file_encoding))
        self.assertEqual(utf16le_file_encoding, "UTF-16")

    def test_file_info(self):
        """
        测试`file_info`方法。
        """
        file = file_info("c:/", "a",
                         "txt", encoding="GBT", C="C",
                         O=20.2, E=True)
        print(file)
        self.assertEqual(str(file), "c:/a.txt")
        print(str(file))
        self.assertEqual(repr(file),
                         "FileInfo{'directory_path': 'c:/', "
                         "'base_name': 'a', 'ext_name': 'txt', 'name': 'a.txt', "
                         "'path': 'c:/a.txt', 'encoding': 'GBT', 'C': 'C', 'O': 20.2, "
                         "'E': True}")
        print(repr(file))

        print(file.C)
        self.assertEqual(file.C, "C")
        print(file.E)
        self.assertEqual(file.E, True)
        print(file.O)
        self.assertEqual(file.O, 20.2)

    def test_get_file_info(self):
        """
        测试`get_file_info`方法。
        """
        file = get_file_info('c:/a.txt', encoding="GBT", C="C",
                             O=20.2, E=True)
        print(file)
        self.assertEqual(str(file), "c:/a.txt")
        print(str(file))
        self.assertEqual(repr(file),
                         "FileInfo{'directory_path': 'c:/', "
                         "'base_name': 'a', 'ext_name': 'txt', 'name': 'a.txt', "
                         "'path': 'c:/a.txt', 'encoding': 'GBT', 'C': 'C', 'O': 20.2, "
                         "'E': True}")
        print(repr(file))

        print(file.C)
        self.assertEqual(file.C, "C")
        print(file.E)
        self.assertEqual(file.E, True)
        print(file.O)
        self.assertEqual(file.O, 20.2)

    def test_get_file_info_of_module(self):
        """
        测试`get_file_info_of_module`方法。
        """
        file = get_file_info_of_module(__name__)
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module(__name__)
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module(__name__)
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module('os')
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module('inspect')
        print(file)
        print(str(file))
        print(repr(file))

        file = get_file_info_of_module('chardet')
        print(file)
        print(str(file))
        print(repr(file))

    # noinspection PyUnresolvedReferences
    def test_file_info_repr(self):
        """
        测试`FileInfo`
        """
        file = FileInfo("c:/", "a",
                        "txt", encoding="GBT", C="C",
                        O=20.2, E=True)
        print(file)
        self.assertEqual(str(file), "c:/a.txt")
        print(str(file))
        self.assertEqual(repr(file),
                         "FileInfo{'directory_path': 'c:/', "
                         "'base_name': 'a', 'ext_name': 'txt', 'name': 'a.txt', "
                         "'path': 'c:/a.txt', 'encoding': 'GBT', 'C': 'C', 'O': 20.2, "
                         "'E': True}")
        print(repr(file))

        print(file.C)
        self.assertEqual(file.C, "C")
        print(file.E)
        self.assertEqual(file.E, True)
        print(file.O)
        self.assertEqual(file.O, 20.2)

    def test_file_info_make_file(self):
        """
        测试`FileInfo`
        """
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)

        test_out = "test_out/file_object"

        dictionary_path = os.path.join(this_file_path, test_out)

        file = FileInfo(dictionary_path, "make_a_file1",
                        "txt", encoding="GBK", C="C",
                        O=20.2, E=True)

        # file.make_directory()
        file.make_file()

    def test_file_object_repr(self):
        """
        测试`FileObject`
        """
        file = FileInfo("c:/", "a",
                        "txt", encoding="GBT", C="C",
                        O=20.2, E=True)
        file_object = FileObject(file)

        print(file_object)
        self.assertEqual(str(file_object), "c:/a.txt")
        print(str(file_object))

        print(repr(file_object))

        print(file_object.C)
        self.assertEqual(file_object.C, "C")
        print(file_object.E)
        self.assertEqual(file_object.E, True)
        print(file_object.O)
        self.assertEqual(file_object.O, 20.2)

    def test_file_object_make_file(self):
        """
        测试`FileObject`
        """
        this_file = __file__
        print("this file: %s" % this_file)
        this_file_path, this_file_name = os.path.split(this_file)
        print('this file name: %s' % this_file_name)
        print('this_file_path: %s' % this_file_path)

        test_out = "test_out/file_object"

        file_path = os.path.join(this_file_path, "{}/make_a_file2.txt".format(test_out))

        file_object = FileObject(file_path, encoding="GBK", C="C", O=20.2, E=True)

        # file.make_directory()
        file_object.make_file()


if __name__ == '__main__':
    unittest.main()
