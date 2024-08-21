#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_unique_object.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试unique_object.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/07     revise
#       Jiwei Huang        0.0.1         2024/08/20     finish
# ------------------------------------------------------------------
# 导包 =============================================================
import unittest

from .unique_object import (UniqueObject,
                            unique_string,
                            random_string)


# 定义 ==============================================================

class TestUniqueObject(unittest.TestCase):
    """
    测试unique_object.py。
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
    def test_unique_string(self):
        print(unique_string())

    def test_random_string(self):
        print(random_string(0))
        print(random_string(1))
        print(random_string(2))
        print(random_string(3))
        print(random_string(4))

    # noinspection PyPropertyAccess,PyUnresolvedReferences
    def test_init(self):
        uo = UniqueObject()
        uo1 = UniqueObject(1, 2, 3)
        uo2 = UniqueObject(1, 2, 3, a=10, b=20)
        print(uo.args)
        print(uo1.args)
        print(uo2.args)
        with self.assertRaises(AttributeError) as context:
            uo.args = (2, 3, 4)
        self.assertEqual("property 'args' of 'UniqueObject' object has no setter", str(context.exception))
        print(context.exception)
        with self.assertRaises(TypeError) as context:
            uo.args[0] = 10
        print(context.exception)
        self.assertEqual("'tuple' object does not support item assignment", str(context.exception))
        print(uo.args)

        print(uo.properties)
        print(uo1.properties)
        print(uo2.properties)
        uo.cc = 10
        uo1.cc = 11
        uo2.cc = 12
        print(uo.properties)
        print(uo1.properties)
        print(uo2.properties)

    # noinspection PyPropertyAccess
    def test_identifier(self):
        uo = UniqueObject()
        uo1 = UniqueObject(1, 2, 3)
        uo2 = UniqueObject(1, 2, 3, a=10, b=20)
        print(uo.identifier)
        print(uo1.identifier)
        print(uo2.identifier)
        with self.assertRaises(AttributeError) as context:
            uo.identifier = "20"
        self.assertEqual("property 'identifier' of 'UniqueObject' object has no setter", str(context.exception))
        print(context.exception)

    def test_equality(self):
        uo = UniqueObject()
        uo1 = UniqueObject()
        uo2 = UniqueObject(1, 2, 3, a=10, b=20)
        uo3 = UniqueObject(1, 2, 3, a=10, b=20)

        self.assertFalse(uo == uo1)
        self.assertTrue(uo1 != uo)
        self.assertTrue(uo2 != uo)
        self.assertTrue(uo3 != uo)

    def test_str(self):
        uo = UniqueObject()
        uo1 = UniqueObject()
        uo2 = UniqueObject(1, 2, 3, a=10, b=20)
        uo3 = UniqueObject(a=10, b=20)
        uo4 = UniqueObject(1, 2, 3)
        print(uo)
        print(uo1)
        print(uo2)
        print(uo3)
        print(uo4)

        uo5 = UniqueObject(a=10, b=20, c=uo)
        print(uo5)

        class Ternary(object):
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

        uo6 = UniqueObject(a=10, b=20, c=Ternary(10, 10, 10))
        print(uo6)

        uo7 = UniqueObject(a=10, b=20, n="dd", c=Ternary(10, 10, 10))
        print(uo7)

    def test_repr(self):
        uo = UniqueObject()
        uo1 = UniqueObject()
        uo2 = UniqueObject(1, 2, 3, a=10, b=20)
        uo3 = UniqueObject(a=10, b=20)
        uo4 = UniqueObject(1, 2, 3)

        print(uo.__repr__())
        print(uo1.__repr__())
        print(uo2.__repr__())
        print(uo3.__repr__())
        print(uo4.__repr__())
        uo5 = UniqueObject(a=10, b=20, c=uo)
        print(uo5.__repr__())

        class Ternary(object):
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

        uo6 = UniqueObject(a=10, b=20, c=Ternary(10, 10, 10))
        print(uo6.__repr__())


if __name__ == '__main__':
    unittest.main()
