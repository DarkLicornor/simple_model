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
            null = Attribute(str, optional=True)
            default_false = Attribute(bool, fallback=False)
        return UUT

    def setUp(self):
        self.uut = self.create_uut()

    def test_model_should_nullify_missing_optional_arguments(self):
        try:
            uut = self.uut(name = 'test', number = 3, allow_missing=True)
            self.assertIsNone(uut.null)
            self.assertIsNotNone(uut.default_false)
            self.assertFalse(uut.default_false)
        except TypeError as e:
            self.fail('creation with missing argument failed in spite of "allow_missing" set to True: ' + str(e))

        with self.assertRaises(ValueError):
            self.uut(name = 'test', allow_missing=True)

    def test_model_should_allow_unknown_arguments_by_default(self):
        try:
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2)

            self.uut._allow_unknown = True
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2)
        except TypeError as e:
            self.fail('creation with unknown argument failed in spite of "allow_unknown" set to True: ' + str(e))

    def test_model_should_not_store_unknown_argument(self):
        try:
            with self.assertRaises(AttributeError):
                self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2, allow_unknown=True).unkown
        except TypeError as e:
            self.fail('creation with unknown argument failed in spite of "allow_unknown" set to True: ' + str(e))

    def test_model_should_be_comparable_to_others(self):
        uut1 = self.uut(name = 'test', number = 3, allow_missing=True)
        uut2 = self.uut(name = 'test', number = 3, allow_missing=True)

        self.assertEquals(uut1, uut2)

        uut3 = self.uut(name = 'test', number = 1, allow_missing=True)

        self.assertNotEquals(uut1, uut3)

    def test_model_should_provide_legacy_attributes_method(self):
        uut = self.uut(name = 'test', number = 3, allow_missing=True)

        self.assertEquals(uut.__attributes__(), dict(uut))

class AttributeTestCase(unittest.TestCase):
    """Tests for the Attribute class"""

    def test_attribute_should_not_be_nullifiable_by_default(self):
        with self.assertRaises(ValueError):
            Attribute(str)(None)

    def test_attribute_should_be_nullifiable_if_specified(self):
        uut = Attribute(str, optional=True)
        try:
            self.assertIsNone(uut(None))
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "optional" set to True: ' + str(e))

    def test_attribute_should_use_fallback_if_specified(self):
        uut = Attribute(str, fallback='test')
        try:
            self.assertEqual(uut(None), 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of fallback being given: ' + str(e))

    def test_attribute_should_call_fallback_if_function(self):
        def test_function():
            return 'test'

        uut = Attribute(str, fallback=test_function)
        try:
            self.assertEqual(uut(None), 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of fallback function being given: ' + str(e))

    def test_attribute_should_cast_value_to_given_type(self):
        try:
            uut = Attribute(str, fallback='test')
            self.assertEqual(uut(12), '12')
            uut = Attribute(int, fallback='test')
            self.assertEqual(uut(12), 12)
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "fallback" set: ' + str(e))

class ExampleTestCase(unittest.TestCase):
    """Tests for the examples"""

    class Data(Model):
        name = Attribute(str)
        some_value = Attribute(str, optional=True)
        another_value = Attribute(int, fallback=0)

    def test_examples(self):
        actual = dict(self.Data(name = 'test', some_value = None, another_value = 12))
        expected = { 'name': 'test', 'some_value': None, 'another_value': 12 }
        self.assertEqual(actual, expected)

        actual = dict(self.Data(name = 'test', allow_missing=True))
        expected = { 'name': 'test', 'some_value': None, 'another_value': 0 }
        self.assertEqual(actual, expected)

        actual = dict(self.Data(name = 'test', unknown_value = True, allow_missing=True, allow_unknown=True))
        expected = { 'name': 'test', 'some_value': None, 'another_value': 0 }
        self.assertEqual(actual, expected)

        init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
        actual = dict(self.Data(**init_dict))
        expected = { 'name': 'test', 'some_value': 'val', 'another_value': 3 }
        self.assertEqual(actual, expected)

    def test_serialization(self):
        import json

        def serialize(model):
            return json.dumps(dict(model))

        def deserialize(string):
            return self.Data(**json.loads(string))

        data = self.Data(name = 'test', some_value = 'val', another_value = 3)

        serialized = serialize(data)
        deserialized = deserialize(serialized)

        self.assertEquals(data, deserialized)

    def test_complex_types(self):
        from datetime import datetime

        def parse_date(string):
            return datetime.strptime(string, '%Y-%m-%d')

        class Data(Model):
            date = Attribute(parse_date)

        expected = { 'date': datetime(2015, 11, 20, 0, 0) }
        actual = dict(Data(date = '2015-11-20'))

        self.assertEquals(actual, expected)

if __name__ == '__main__':
    unittest.main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
