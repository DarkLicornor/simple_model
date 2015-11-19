#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import unittest

from simple_model import Model, Attribute

class ModelTestCase(unittest.TestCase):
    """Tests for the Model class"""

    def create_uut(self):
        class UUT(Model):
            name = Attribute(str)
            number = Attribute(int)
            null = Attribute(str, nullable=True)
            default_false = Attribute(bool, fallback=False)
        return UUT

    def setUp(self):
        self.uut = self.create_uut()

    def test_model_should_not_allow_missing_arguments_by_default(self):
        with self.assertRaises(TypeError):
            self.uut(name = 'test', number = 3, default_false = True)

    def test_model_should_nullify_missing_nullable_arguments_if_specified(self):
        try:
            uut = self.uut(name = 'test', number = 3, _allow_missing=True)
            self.assertIsNone(uut.null)
            self.assertIsNotNone(uut.default_false)
            self.assertFalse(uut.default_false)
        except TypeError as e:
            self.fail('creation with missing argument failed in spite of "_allow_missing" set to True: ' + str(e))

        with self.assertRaises(ValueError):
            self.uut(name = 'test', _allow_missing=True)

    def test_model_should_not_allow_unknown_arguments_by_default(self):
        with self.assertRaises(TypeError):
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2)

    def test_model_should_allow_unknown_arguments_if_specified(self):
        try:
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2, _allow_unknown=True)

            self.uut.__allow_unknown__ = True
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2)
        except TypeError as e:
            self.fail('creation with unknown argument failed in spite of "allow_unknown" set to True: ' + str(e))

    def test_model_should_not_store_unknown_argument(self):
        try:
            with self.assertRaises(AttributeError):
                self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2, _allow_unknown=True).unkown
        except TypeError as e:
            self.fail('creation with unknown argument failed in spite of "_allow_unknown" set to True: ' + str(e))


class AttributeTestCase(unittest.TestCase):
    """Tests for the Attribute class"""

    def test_attribute_should_not_be_nullifiable_by_default(self):
        with self.assertRaises(ValueError):
            Attribute(str)(None)

    def test_attribute_should_be_nullifiable_if_specified(self):
        uut = Attribute(str, nullable=True)
        try:
            self.assertIsNone(uut(None))
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "__nullable__" set to True: ' + str(e))

    def test_attribute_should_use_fallback_if_specified(self):
        uut = Attribute(str, fallback='test')
        try:
            self.assertEqual(uut(None), 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "__nullable__" set to True: ' + str(e))

    def test_attribute_should_cast_value_to_given_type(self):
        try:
            uut = Attribute(str, fallback='test')
            self.assertEqual(uut(12), '12')
            uut = Attribute(int, fallback='test')
            self.assertEqual(uut(12), 12)
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "fallback" set: ' + str(e))

if __name__ == '__main__':
    unittest.main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
