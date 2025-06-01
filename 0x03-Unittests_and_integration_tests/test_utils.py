#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map and utils.get_json.
"""
import unittest
from unittest.mock import patch, Mock # Added Mock for configuring the return value of the patched object
from parameterized import parameterized
# Assuming utils.py is in the same directory or PYTHONPATH
from utils import access_nested_map, get_json # Added get_json
from typing import Mapping, Sequence, Any, Dict


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
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_missing_key: str
    ) -> None:
        """
        Tests that `access_nested_map` raises a KeyError for specific invalid paths
        and verifies that the missing key is part of the exception.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_missing_key}'")


class TestGetJson(unittest.TestCase):
    """
    Test suite for the `get_json` function from the `utils` module.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get') # Patch 'requests.get' within the 'utils' module
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict[str, Any],
            mock_requests_get: Mock # The patch decorator passes the mock object as an argument
    ) -> None:
        """
        Tests that `utils.get_json` fetches from the correct URL and returns
        the expected JSON payload, by mocking `requests.get`.

        Args:
            test_url (str): The URL to pass to `get_json`.
            test_payload (Dict[str, Any]): The expected JSON payload to be returned.
            mock_requests_get (Mock): The mock object for `requests.get` injected by @patch.
        """
        # Configure the mock object:
        # 1. We need `requests.get(url)` to return an object...
        # 2. ...that has a `json()` method...
        # 3. ...and that `json()` method should return `test_payload`.

        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        # mock_response.raise_for_status = Mock() # If get_json calls raise_for_status

        # Configure the patched 'requests.get' to return this mock_response
        mock_requests_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assertions:
        # 1. Test that the mocked get method was called exactly once with test_url as argument.
        mock_requests_get.assert_called_once_with(test_url)

        # 2. Test that the output of get_json is equal to test_payload.
        self.assertEqual(result, test_payload)

# if __name__ == '__main__':
#     unittest.main()