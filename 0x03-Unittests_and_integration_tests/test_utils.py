#!/usr/bin/env python3
"""
Unit tests for utils.py functions.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

# Assuming utils.py is in the same dir or PYTHONPATH correctly set
from utils import access_nested_map, get_json, memoize
from typing import (  # Break long import for E501
    Mapping, Sequence, Any, Dict, List  # Added List back from your code
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
            nested_map: Dict[str, Any],  # Using Dict/List from your code
            path: List[str],
            expected: Any
            ) -> None:
        """
        Test that `access_nested_map` returns the correct value for valid inputs.
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
        Test `access_nested_map` raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Unit test for the `get_json` function."""  # Fixed potential E501

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    # Your version used manual patcher.start/stop.
    # Reverting to that to match your code, ensuring it's styled.
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict
            ) -> None:  # Fixed potential E501
        """Test that get_json fetches correct value with mocked requests.get."""
        config = {'return_value.json.return_value': test_payload}
        # Patching 'requests.get' directly as it's imported in utils.py
        # or 'utils.requests.get' if requests is imported inside utils module
        # Assuming 'utils.requests.get' for safety if 'requests' is namespaced
        patcher = patch('utils.requests.get', **config)
        mock_get_method = patcher.start()

        self.assertEqual(get_json(test_url), test_payload)
        mock_get_method.assert_called_once_with(test_url)

        patcher.stop()


class TestMemoize(unittest.TestCase):
    """Unit tests for the `memoize` decorator."""  # Fixed potential E501

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

        # This is where your line 84 (E501) might have been.
        # Breaking 'with patch.object(...)' for style.
        with patch.object(
                TestClass,
                "a_method",
                return_value=42  # Mocked return for a_method
                ) as mock_a_method:
            test_instance = TestClass()

            # These calls and assertions are where line 99 (E127) and 101 (E124)
            # might have been reported. Ensure they are indented correctly.
            # Standard 4-space indent from the 'with' line.
            result_one = test_instance.a_property()  # First call
            result_two = test_instance.a_property()  # Second call (should be cached)

            self.assertEqual(result_one, 42)
            self.assertEqual(result_two, 42)
            mock_a_method.assert_called_once()


