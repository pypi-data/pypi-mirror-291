#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_data_capsule.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试data_capsule.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/12/30     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     finish
# ------------------------------------------------------------------
# 导包 =============================================================
import unittest
import numpy as np
import pandas as pd
from .data_capsule import DataCapsule


# ==================================================================
class TestDataCapsule(unittest.TestCase):
    """
    测试data_capsule.py。
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
    def test_item_name_prefix(self):
        """
        测试：data_capsule.__DEFAULT_ITEM_NAME_PREFIX__
        """
        from . import data_capsule
        print(data_capsule.__DEFAULT_ITEM_NAME_PREFIX__)
        self.assertEqual("item_", data_capsule.__DEFAULT_ITEM_NAME_PREFIX__)

    def test_constructor(self):
        """
        测试DataCapsule的构造方法1。
        """
        pd.set_option('display.max_columns', None)
        # 设置pandas显示所有行
        pd.set_option('display.max_rows', None)
        # 设置pandas显示所有字符
        pd.set_option('display.max_colwidth', None)
        print(bool(None))

        print("-------------------------------------")
        table1 = DataCapsule()
        self.assertEqual(True, table1.is_empty)
        print(table1.shape)
        self.assertEqual((0, 0), table1.shape)
        # self.assertEqual(table1)
        table1.print_data()
        print("-------------------------------------")

        table2 = DataCapsule(1)
        self.assertEqual(False, table2.is_empty)
        print(table2.shape)
        self.assertEqual((1, 1), table2.shape)
        table2.print_data()
        print("-------------------------------------")

        table3 = DataCapsule(1, 2)
        print(table3.shape)
        self.assertEqual((1, 2), table3.shape)
        table3.print_data()
        print("-------------------------------------")

        table4 = DataCapsule(1, 2, [1])
        print(table4.shape)
        self.assertEqual((1, 3), table4.shape)
        table4.print_data()
        print("-------------------------------------")

        table5 = DataCapsule([1])
        print(table5.shape)
        table5.print_data()
        print("-------------------------------------")

        table6 = DataCapsule([1, 2])
        print(table6.shape)
        table6.print_data()
        print("-------------------------------------")

        table7 = DataCapsule([1], [1])
        print(table7.shape)
        table7.print_data()
        print("-------------------------------------")

        table8 = DataCapsule([1], [1, 2])
        print(table8.shape)
        table8.print_data()
        print("-------------------------------------")

        table9 = DataCapsule([1, 3, 5], [1, 2])
        print(table9.shape)
        table9.print_data()
        print("-------------------------------------")

        table10 = DataCapsule([1, 3, 5], [1, 2], 2)
        print(table10.shape)
        table10.print_data()
        print("-------------------------------------")

        table11 = DataCapsule(1, 3, 'a', [1, 3, 5], [1, 2], 2)
        print(table11.shape)
        table11.print_data()
        print("-------------------------------------")

        table12 = DataCapsule(4, '5', [object], [1, 3, 5], [1, 2], 2)
        print(table12.shape)
        table12.print_data()
        print("-------------------------------------")

        table13 = DataCapsule(1, 3, True, [1, 3, 5], [1, 2], 2)
        print(table13.shape)
        table13.print_data()
        print("-------------------------------------")

        table14 = DataCapsule(4, '5', object, [1, 3, 5], [1, 2], 2)
        print(table14.shape)
        table14.print_data()
        print("-------------------------------------")

        table15 = DataCapsule(4, '5', table14, [1, 3, 5], [1, 2], 2)
        print(table15.shape)
        table15.print_data()
        print("-------------------------------------")

        table16 = DataCapsule(None)
        print(table16.shape)
        table16.print_data()

    def test_constructor2(self):
        table1 = DataCapsule(1, item_names={0: 'one'})
        print(table1.shape)
        table1.print_data()
        table2 = DataCapsule(1, item_names={0: 'one', 1: 'two'})
        print(table2.shape)
        table2.print_data()

        table3 = DataCapsule(1, 2, 3, 4, item_names={0: 'one', 1: 'two'})
        print(table3.shape)
        table3.print_data()

        table4 = DataCapsule(1, 2, 3, 4, item_names={1: 'one', 2: 'two'})
        print(table4.shape)
        table4.print_data()

        table5 = DataCapsule(1, 2, 3, 4, item_names={1: 'one', 2: 'two', 3: 'three', 5: 'five'})
        print(table5.shape)
        table5.print_data()

    def test_constructor3(self):
        table1 = DataCapsule(1,
                             item_names=['one'])
        print(table1.shape)
        table1.print_data()

        table2 = DataCapsule(1,
                             item_names=['one', 'two'])
        print(table2.shape)
        table2.print_data()

        table3 = DataCapsule(1, 2, 3, 4,
                             item_names=['one', 'two'])
        print(table3.shape)
        table3.print_data()

        table4 = DataCapsule(1, 2, 3, 4,
                             item_names=['one', 'two', 'three'])
        print(table4.shape)
        table4.print_data()

        table5 = DataCapsule(1, 2, 3, 4,
                             item_names=['one', 'two', 'three', 'five'])
        print(table5.shape)
        table5.print_data()

    def test_update_item(self):
        table = DataCapsule()
        print(table.shape)
        table.print_data()
        table.update_item(2, '0')
        print(table.shape)
        table.print_data()

        table2 = DataCapsule(1, 2, 3, 4,
                             item_names=['one', 'two', 'three', 'five'])
        print(table2.shape)
        table2.print_data()
        table2.update_item(2, '0')
        print(table2.shape)
        table2.print_data()

        table3 = DataCapsule(1, 2, 3, 4,
                             item_names=['one', 'two', 'three', 'five'])
        print(table3.shape)
        table3.print_data()
        table3.update_item([2, 0, 3, 4], '0')
        print(table3.shape)
        table3.print_data()

        table4 = DataCapsule(1, 2, 3, 4,
                             item_names=['one', 'two', 'three', 'five'])
        print(table4.shape)
        table4.print_data()
        table4.update_item([2, 0, 3, 4])
        table4.update_item([2, 0, 3, 4])
        table4.update_item([2, 0, 3, 4])
        table4.update_item([2, 0, 3, 4])
        print(table4.shape)
        table4.print_data()

    def test_get_item(self):
        table3 = DataCapsule(1, [1, 2], None, (4, 5, 6, 7), np.arange(20),
                             item_names=['one', 'two', 'three', 'five'])
        table3.print_data({'display.max_columns': None, 'display.max_rows': None,
                           'display.max_colwidth': None})

        print(table3.get_item('one'))
        print(table3.get_item('two'))
        print(table3.get_item('three'))
        print(table3.get_item('five'))
        print(table3.get_item('item_4'))

        print(table3.get_item(0))
        print(table3.get_item(1))
        print(table3.get_item(2))
        print(table3.get_item(3))
        print(table3.get_item(4))

    def test_update_data(self):
        table3 = DataCapsule(1, [1, 2], None, (4, 5, 6, 7), np.arange(20),
                             item_names=['one', 'two', 'three', 'five'])
        table3.print_data({'display.max_columns': None, 'display.max_rows': None,
                           'display.max_colwidth': None})
        table3.update_data(1, 2, 3, 4,
                           item_names=['one', 'two', 'three', 'five'])
        table3.print_data({'display.max_columns': None, 'display.max_rows': None,
                           'display.max_colwidth': None})

    def test_update_data2(self):
        table3 = DataCapsule(1, [1, 2], None, (4, 5, 6, 7), np.arange(20),
                             item_names=['one', 'two', 'three', 'five'])
        table3.print_data({'display.max_columns': None, 'display.max_rows': None,
                           'display.max_colwidth': None})
        table3.update_data(1, 2, 3, 4,
                           item_names=['one1', 'two1', 'three1', 'five1'])
        table3.print_data({'display.max_columns': None, 'display.max_rows': None,
                           'display.max_colwidth': None})


if __name__ == '__main__':
    unittest.main()
