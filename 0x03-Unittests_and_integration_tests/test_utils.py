#!/usr/bin/env python3
"""
Unit tests for utils.py functions.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` function.
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
            expected: Any
            ) -> None:
        """Test access_nested_map with various inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_key: str
            ) -> None:
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Test suite for the `get_json` function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            mock_get: Mock
            ) -> None:
        """Test get_json with mocked HTTP calls."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test suite for the `memoize` decorator.
    """

    def test_memoize(self) -> None:
        """
        Tests that the `memoize` decorator caches the result of a method
        and calls the underlying method only once.
        """

        class TestClass:
            """A test class with a method and a memoized property-like method."""
            def a_method(self) -> int:
                """A sample method that returns a fixed value."""
                return 42

            @memoize  
            def a_property(self) -> int:
                """A property-like method that calls a_method, memoized."""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(
                test_obj,
                'a_method',
                return_value=42
                ) as mock_a_method:
            result1 = test_obj.a_property()
            result2 = test_obj.a_property()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()


