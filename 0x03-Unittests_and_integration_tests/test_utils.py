#!/usr/bin/env python3
"""We are testing utils.access_nested_map from this same directory"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch, Mock


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

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception_ou):
        """Testing exceptions for specified inputs using parameterized"""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
            self.assertEqual(exception_ou, e.exception)


class TestGetJson(unittest.TestCase):
    """ Json format testing """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """Testing get_json function using parameterized decorator & patching
            requests.get
        """
        # Create a Mock object with json method that returns test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch('requests.get', return_value=mock_response):
            # Call the get_json function with the test_url
            result = get_json(test_url)
            self.assertEqual(result, test_payload)

            # Assert that mocked get method was called once with test_url
            mock_response.json.assert_called_once()


if __name__ == "__main__":
    unittest.main()
