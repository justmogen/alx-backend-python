#!/usr/bin/env python3
"""We are testing utils.access_nested_map from this same directory"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """testing using parameterized decorator"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """the tst case"""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    def test_access_nested_map_exception(self):
        """testing for exception"""
        nested_map = {"a": {"b": 2}}
        path = ("a", "c")
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual('c', e.exception.args[0])


if __name__ == "__main__":
    unittest.main()
