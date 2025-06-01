#!/usr/bin/env python3
"""
Unit tests for utils.py functions.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

# Assuming utils.py is in the same dir or PYTHONPATH correctly set.
# If utils.py in the parent directory of 0x03-Unittests_and_integration_tests
# and you are running tests from 0x03-Unittests_and_integration_tests:
# You might need to adjust sys.path if 'from utils import ...' fails.
# However, standard 'python -m unittest test_utils.py' from the project root
# or 'python -m unittest 0x03-Unittests_and_integration_tests.test_utils'
# should handle imports correctly if utils.py is at the root of where Python
# starts looking (e.g., if 0x03-Unittests_and_integration_tests is a package
# or utils.py is also in 0x03-Unittests_and_integration_tests, or project root
# is in PYTHONPATH).
# For ALX structure, utils.py is often at the root of the task folder.
from utils import access_nested_map, get_json, memoize
from typing import (
    Mapping, Sequence, Any, Dict, List
)


class TestAccessNestedMap(unittest.TestCase):
    """Unit test for the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict[str, Any],
            path: List[str],
            expected: Any
            ) -> None:
        """
        Test that `access_nested_map` returns the correct value for valid
        inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a"], "a"),
        ({"a": 1}, ["a", "b"], "b")
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict[str, Any],
            path: List[str],
            expected_key: str
            ) -> None:
        """
        Test `access_nested_map` raises KeyError for invalid paths and checks
        the exception message.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Unit test for the `get_json` function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict
            ) -> None:
        """Test that get_json fetches correct value mocked requests.get."""
        # Configuration for the mock object's return_value.json() method
        config = {'return_value.json.return_value': test_payload}

        # Use patch as a context manager for cleaner start/stop
        # Patch 'utils.requests.get' as get_json in utils.py calls requests.get
        with patch('utils.requests.get', **config) as mock_get_method:
            # Call the function under test
            self.assertEqual(get_json(test_url), test_payload)

            # Verify that requests.get was called once with the test_url
            mock_get_method.assert_called_once_with(test_url)
        # No manual patcher.stop() needed with 'with' statement


class TestMemoize(unittest.TestCase):
    """Unit tests for the `memoize` decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result of a method call."""
        class TestClass:
            """A Test Class for handling methods that are memoized."""

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

        # Patch 'a_method' on the TestClass.
        # This means any instance of TestClass created inside this 'with'
        # block will have its 'a_method' mocked.
        with patch.object(
                TestClass,
                "a_method",
                return_value=42  # Ensure the mock returns the expected value
                ) as mock_a_method:
            test_instance = TestClass()

            # Call a_property twice
            result_one = test_instance.a_property()  # First call, should call
            # a_method
            result_two = test_instance.a_property()  # Second call, should use
            # cache

            # Assertions
            self.assertEqual(result_one, 42)
            self.assertEqual(result_two, 42)
            mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
    