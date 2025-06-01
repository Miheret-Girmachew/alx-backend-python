#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map and other utility functions.
"""
import unittest
from parameterized import parameterized # No need for parameterized_class for this task
from utils import access_nested_map # Assuming utils.py is accessible
from typing import Mapping, Sequence, Any, Type # Added Type for exception type hint


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
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_output)

    @parameterized.expand([
        # Input 1: nested_map={}, path=("a",)
        # Expected: KeyError with a message containing 'a'
        ({}, ("a",), "a"),

        # Input 2: nested_map={"a": 1}, path=("a", "b")
        # Expected: KeyError with a message containing 'b'
        # This depends on access_nested_map raising KeyError for this case.
        # If it raises TypeError, this test case would need to expect TypeError.
        # The task *specifies* testing for KeyError.
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_missing_key: str # The key that is expected to be missing/problematic
    ) -> None:
        """
        Tests that `access_nested_map` raises a KeyError for specific invalid paths
        and verifies that the missing key is part of the exception.
        """
        # The context manager self.assertRaises(KeyError) ensures a KeyError is raised.
        # It also provides the exception instance as `cm.exception`.
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        
        # Check that the exception message is the missing key itself,
        # as KeyError(key) will have `key` as its first argument.
        # str(cm.exception) typically yields "'key'".
        # We are checking if the actual missing key string is what the KeyError reports.
        self.assertEqual(str(cm.exception), f"'{expected_missing_key}'")

# if __name__ == '__main__':
#     unittest.main()