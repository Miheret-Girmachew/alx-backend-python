#!/usr/bin/env python3
"""
This module contains unit tests for the utility functions:
- access_nested_map
- get_json
- memoize
"""

import unittest
from typing import Dict, List, Any  # For type hinting test cases
from unittest.mock import patch, Mock  # Added Mock for TestGetJson
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit test for the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: List[str], expected: Any
    ):  # Line break for E501 if signature was too long
        """
        Test that `access_nested_map` returns the correct value when
        given valid nested maps and path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a"], "a"),  # Added expected key for message check
        ({"a": 1}, ["a", "b"], "b")  # Added expected key for message check
    ])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: List[str], expected_key: str
    ) -> None:
        """
        Test that `access_nested_map` raises a KeyError when the path
        doesn't exist in the nested map and checks message.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Assuming KeyError message is "'key'" based on previous task
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Unit test for the `get_json` function in `utils`"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """Test that get_json fetches correct value with mocked requests.get."""
        # Configure the mock for requests.get().json()
        # This creates a mock object that, when its json() method is called,
        # returns test_payload.
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch 'utils.requests.get' because get_json in utils.py calls requests.get
        with patch('utils.requests.get', return_value=mock_response) as mock_actual_get:
            # Call the function under test
            result = get_json(test_url)

            # Assert that requests.get was called once with the test_url
            mock_actual_get.assert_called_once_with(test_url)
            # Assert that the result of get_json is the test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the `memoize` decorator from the `utils` module."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result of a method call."""
        class TestClass:
            """A Test Class for handling methods that are memoized.""" # Corrected typo

            def a_method(self) -> int:
                """A simple method that returns a constant value."""
                return 42

            @memoize
            def a_property(self) -> int:
                """
                A property-like method that calls a_method.
                This call should be memoized.
                """
                return self.a_method()

        # This is the block where line 84 (E501) and line 99 (E127)
        # were likely reported from in your version.
        # In your original code, this was:
        # with patch.object(TestClass, "a_method") as mock:
        # Let's assume `return_value=42` was intended to be part of the patch
        # to ensure `a_property` gets a consistent value from the mocked `a_method`.
        with patch.object(
                TestClass,
                "a_method",
                return_value=42  # Ensure mocked method returns what a_property expects
                ) as mock_a_method:  # Renamed 'mock' to 'mock_a_method' for clarity
            
            test_instance = TestClass()  # Create an instance

            # Call a_property twice
            result_1 = test_instance.a_property()
            result_2 = test_instance.a_property()

            # Assertions:
            # Correct indentation for these lines (likely your line 99 was one of these)
            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42) # Should return cached result
            mock_a_method.assert_called_once() # a_method should only be called once


if __name__ == '__main__':
    unittest.main()

# Make sure there's one newline character after this line (for W292)