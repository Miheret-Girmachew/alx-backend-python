#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map # Assuming utils.py is in the same directory or PYTHONPATH
from typing import Mapping, Sequence, Any, Dict, Tuple # For type hinting test cases


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` function from the `utils` module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_output: Any
    ) -> None:
        """
        Tests that `access_nested_map` returns the correct output for various inputs.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The path of keys to follow.
            expected_output (Any): The expected value at the end of the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_output)

    @parameterized.expand([
        ({}, ("a",), KeyError), # Test case: empty map, path ("a",) should raise KeyError
        ({"a": 1}, ("a", "b"), TypeError), # Test case: trying to access a sub-key from a non-mapping
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_exception: Exception # Type hint for the expected exception class
    ) -> None:
        """
        Tests that `access_nested_map` raises the appropriate exceptions for invalid paths.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The path of keys to follow.
            expected_exception (Exception): The type of exception expected to be raised.
        """
        with self.assertRaises(expected_exception) as context:
            access_nested_map(nested_map, path)
        # Optionally, you can assert specifics about the exception, e.g., message or args
        # For KeyError, the argument is the key that was not found.
        # For this task, just raising the correct type is sufficient based on instruction.
        # if expected_exception == KeyError:
        #     self.assertEqual(str(context.exception), f"'{path[-1]}'") # Check the missing key if path is not empty

if __name__ == '__main__':
    unittest.main()