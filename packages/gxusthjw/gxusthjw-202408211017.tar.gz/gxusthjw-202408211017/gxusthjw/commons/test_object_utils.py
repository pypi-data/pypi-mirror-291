#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_object_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试object_utils.py。
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
import unittest
from .object_utils import (hash_code,
                           gen_hash,
                           safe_repr,
                           get_methods_and_attributes)

from .gxusthjw_base import Version, Author, Copyright


# ==================================================================


class TestObjectUtils(unittest.TestCase):
    """
    测试object_utils.py。
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

    def test_hash_code(self):
        """
        测试hash_code方法。

        :return: None
        """
        print(hash_code(0))
        print(hash_code(0, 1))
        print(hash_code(0, 1, 1.0, 2.0))
        print(hash_code(0, object, "d"))
        print(hash_code(0, 1, 1.0, 2.0, "dd"))
        print(hash_code(0, 1, 1.0, 2.0, (1, 2, 3, 4)))

    def test_gen_hash(self):
        """
        测试arrays.hash_code方法。

        :return: None
        """
        print(gen_hash(0))
        print(gen_hash(0, 1))
        print(gen_hash(0, 1, 1.0, 2.0))
        print(gen_hash(0, object, "d"))
        print(gen_hash(0, 1, 1.0, 2.0, "dd"))
        print(gen_hash(0, 1, 1.0, 2.0, (1, 2, 3, 4)))

    def test_safe_repr(self):
        """
        测试safe_repr函数。
        """
        author = Author()
        version = Version()
        copyright1 = Copyright()
        print(safe_repr(author))
        self.assertEqual(
            "{Jiwei Huang,('jiweihuang@vip.163.com', "
            "'jiweihuang@yeah.net', 'huangjiwei@gxust.edu.cn'),"
            "('Guangxi University of Science and Technology',)}",
            safe_repr(author))
        print(safe_repr(version))
        self.assertEqual("(1,0,0,0)", safe_repr(version))
        print(safe_repr(copyright1))
        self.assertEqual(
            "(Copyright (c) 2012-2023, Jiwei Huang. All Rights Reserved.,())",
            safe_repr(copyright1))

        print(safe_repr(author, short=True, max_length=20))
        self.assertEqual("{Jiwei Huang,('jiwei [truncated]...",
                         safe_repr(author, short=True, max_length=20))

    def test_get_methods_and_attributes(self):
        import tkinter as tk
        root = tk.Tk()
        top = tk.Toplevel(root)
        methods, attributes = get_methods_and_attributes(top)
        print(methods)
        print(attributes)

        class MethodsAttributes(object):
            def __init__(self):
                self.__a = 1
                self.b = 2

            @property
            def a(self):
                return self.__a

            # noinspection PyMethodMayBeStatic
            def c(self, d):
                return d

            @property
            def e(self):
                return self.__a + 10

            @e.setter
            def e(self, v):
                self.__a = v - 10

        ma = MethodsAttributes()
        methods, attributes = get_methods_and_attributes(ma)
        print(methods)
        print(attributes)

        c_method = getattr(ma, methods[0])
        print(c_method(10))


        setattr(ma, attributes[1], 100)
        setattr(ma, attributes[2], 200)

        print(ma.a)
        print(ma.b)


if __name__ == '__main__':
    unittest.main()
