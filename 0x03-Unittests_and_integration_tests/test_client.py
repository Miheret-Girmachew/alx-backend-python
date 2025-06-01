#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock # Added PropertyMock, though not used yet
from parameterized import parameterized, parameterized_class # Added parameterized_class
# Assuming client.py is in the same directory or PYTHONPATH
from client import GithubOrgClient
from typing import Dict, Any


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1342004, "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ="}),
        ("abc", {"login": "abc", "id": 322224, "node_id": "MDEyOk9yZ2FuaXphdGlvbjMyMjIyNA=="}),
        # Added a more generic payload structure for the second case
    ])
    @patch('client.get_json') # Patch get_json where it's used within client.py
    def test_org(
            self,
            org_name: str,
            expected_payload: Dict[str, Any],
            mock_get_json: Mock  # Injected by @patch
            ) -> None:
        """
        Tests that `GithubOrgClient.org` returns the correct value
        by mocking the `get_json` call.

        Args:
            org_name (str): The organization name to test.
            expected_payload (Dict[str, Any]): The expected dictionary payload
                                             that `get_json` should effectively return.
            mock_get_json (Mock): The mock object for `get_json`.
        """
        # Configure the mock_get_json to return the expected_payload
        # when it's called by client.GithubOrgClient.org()
        mock_get_json.return_value = expected_payload

        # Instantiate the client with the current org_name
        client_instance = GithubOrgClient(org_name)

        # Call the .org() method
        result = client_instance.org()

        # 1. Assert that get_json was called once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # 2. Assert that the result of client_instance.org() is the expected_payload
        self.assertEqual(result, expected_payload)


# To run tests directly from this file (optional for ALX, but good for local dev)
# if __name__ == '__main__':
#     unittest.main()

# Ensure a single newline at the end of the file for Pycodestyle (W292)