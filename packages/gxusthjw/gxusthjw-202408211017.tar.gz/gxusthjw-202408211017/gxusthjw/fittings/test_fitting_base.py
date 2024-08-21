#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_fitting_base.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 测试fitting_base.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/08/18     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import unittest
from typing import Optional, Union

import numpy as np
import numpy.typing as npt

from .fitting_base import FittingBase


# ==================================================================
class TestFittingBase(unittest.TestCase):
    """
    测试fitting_base.py。
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
    # noinspection DuplicatedCode
    def test_init(self):
        class FittingImpl(FittingBase):

            def __init__(self, y: npt.ArrayLike,
                         x: Optional[npt.ArrayLike] = None,
                         start: Optional[int] = None,
                         length: Optional[int] = None,
                         method: Optional[Union[str, int]] = None,
                         **kwargs):
                super().__init__(y, x, start, length, method, **kwargs)

            def fit(self, **kwargs):
                pass

            def interactive_fit(self, **kwargs):
                pass

        # -----------------------------------------------
        x = np.arange(10)
        y = 3 * x + 20

        fb = FittingImpl(y)
        self.assertIsInstance(fb, FittingBase)
        self.assertTrue(np.allclose(y, fb.y))
        self.assertTrue(np.allclose(x, fb.x))
        self.assertEqual(fb.method, None)
        self.assertEqual(fb.start, 0)
        self.assertEqual(fb.length, 10)
        self.assertEqual(fb.y_len, 10)
        self.assertEqual(fb.x_len, 10)
        self.assertEqual(np.allclose(x, fb.x_var), True)
        self.assertEqual(np.allclose(y, fb.y_var), True)

        fb1 = FittingImpl(y, x)
        self.assertIsInstance(fb1, FittingBase)
        self.assertTrue(np.allclose(y, fb1.y))
        self.assertTrue(np.allclose(x, fb1.x))
        self.assertEqual(fb1.method, None)
        self.assertEqual(fb1.start, 0)
        self.assertEqual(fb1.length, 10)
        self.assertEqual(fb1.y_len, 10)
        self.assertEqual(fb1.x_len, 10)
        self.assertEqual(np.allclose(x, fb1.x_var), True)
        self.assertEqual(np.allclose(y, fb1.y_var), True)

        fb2 = FittingImpl(y, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertIsInstance(fb2, FittingBase)
        self.assertTrue(np.allclose(y, fb2.y))
        self.assertTrue(np.allclose(np.asarray([1, 2, 3, 4, 5, 6, 7, 8]), fb2.x))
        self.assertEqual(fb2.method, None)
        self.assertEqual(fb2.start, 0)
        self.assertEqual(fb2.length, 8)
        self.assertEqual(fb2.y_len, 10)
        self.assertEqual(fb2.x_len, 8)
        self.assertEqual(np.allclose([1, 2, 3, 4, 5, 6, 7, 8], fb2.x_var), True)
        self.assertEqual(np.allclose(y[:8], fb2.y_var), True)

        fb3 = FittingImpl(y, [1, 2, 3, 4, 5, 6, 7, 8], start=1)
        self.assertIsInstance(fb3, FittingBase)
        self.assertTrue(np.allclose(y, fb3.y))
        self.assertTrue(np.allclose(np.asarray([1, 2, 3, 4, 5, 6, 7, 8]), fb3.x))
        self.assertEqual(fb3.method, None)
        self.assertEqual(fb3.start, 1)
        self.assertEqual(fb3.length, 7)
        self.assertEqual(fb3.y_len, 10)
        self.assertEqual(fb3.x_len, 8)
        self.assertEqual(np.allclose([2, 3, 4, 5, 6, 7, 8], fb3.x_var), True)
        self.assertEqual(np.allclose(y[1:8], fb3.y_var), True)

        fb4 = FittingImpl(y, [1, 2, 3, 4, 5, 6, 7, 8], start=1, method="oo")
        self.assertIsInstance(fb4, FittingBase)
        self.assertTrue(np.allclose(y, fb4.y))
        self.assertTrue(np.allclose(np.asarray([1, 2, 3, 4, 5, 6, 7, 8]), fb4.x))
        self.assertEqual(fb4.method, 'oo')
        self.assertEqual(fb4.start, 1)
        self.assertEqual(fb4.length, 7)
        self.assertEqual(fb4.y_len, 10)
        self.assertEqual(fb4.x_len, 8)
        self.assertEqual(np.allclose([2, 3, 4, 5, 6, 7, 8], fb4.x_var), True)
        self.assertEqual(np.allclose(y[1:8], fb4.y_var), True)


if __name__ == '__main__':
    unittest.main()
