#!/usr/bin/env python3
"""
Unit tests for utils.py functions.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

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
        Test `access_nested_map` raises KeyError for invalid paths.
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
        config = {'return_value.json.return_value': test_payload}
        patcher = patch('utils.requests.get', **config)
        mock_get_method = patcher.start()

        self.assertEqual(get_json(test_url), test_payload)
        mock_get_method.assert_called_once_with(
            test_url
        )

        patcher.stop()


class TestMemoize(unittest.TestCase):
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
        with patch.object(
                TestClass,
                "a_method",
                return_value=42  
                ) as mock_a_method:
            test_instance = TestClass()
            result_one = test_instance.a_property()  
            result_two = test_instance.a_property()  
            self.assertEqual(result_one, 42)
            self.assertEqual(result_two, 42)
            mock_a_method.assert_called_once()