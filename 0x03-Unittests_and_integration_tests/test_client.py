#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock # Import PropertyMock
from parameterized import parameterized
# Ensure client.py and utils.py are accessible
from client import GithubOrgClient
from typing import Dict, Any


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1, "repos_url": "google_repos_url_payload"}),
        ("abc", {"login": "abc", "id": 2, "repos_url": "abc_repos_url_payload"}),
    ])
    @patch('client.get_json')  # Patch get_json where it is looked up (in client.py)
    def test_org(
            self,
            org_name: str,
            expected_org_payload: Dict,
            mock_get_json: Mock
            ) -> None:
        """
        Tests that `GithubOrgClient.org` returns the correct value by mocking
        the `get_json` call it makes.
        """
        # Configure the mock_get_json to return the predefined payload
        mock_get_json.return_value = expected_org_payload

        # Instantiate the client
        client_instance = GithubOrgClient(org_name)

        # Call the .org() method (this will use the mocked get_json)
        result_org_data = client_instance.org()

        # Assert that get_json was called once with the correct URL
        expected_api_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_api_url)

        # Assert that the .org() method returned the expected payload
        self.assertEqual(result_org_data, expected_org_payload)

    def test_public_repos_url(self) -> None:
        """
        Tests the `_public_repos_url` property.
        It mocks the `GithubOrgClient.org` method to control the payload it returns,
        from which `_public_repos_url` derives its value.
        """
        # This is the known payload that our mocked `org` method will return.
        # It must contain the 'repos_url' key.
        known_org_payload = {
            "repos_url": "https://api.github.com/orgs/specific_org/repos"
        }
        expected_repos_url_value = "https://api.github.com/orgs/specific_org/repos"

        # We patch `GithubOrgClient.org`. Since `_public_repos_url` calls `self.org()`,
        # we mock this `org` method.
        # `PropertyMock` is used if `org` itself were a @property.
        # Since `org` is a method (even if @memoized), `patch.object` for a method
        # or simply `@patch` on the method path is appropriate.
        # The task says "patch GithubOrgClient.org and make it return a known payload."
        # And "memoize turns methods into properties" is a general hint for the _public_repos_url test context.
        # For mocking `org` which is called as `self.org()`, a standard mock is fine.
        # The key is that `_public_repos_url` is a @property.

        with patch.object(
                GithubOrgClient,
                'org',  # The method to patch on the class
                # new_callable=PropertyMock # Use this if 'org' itself is a @property
                # If 'org' is a method (even if @memoized), PropertyMock is not needed here.
                # We want to control what `client_instance.org()` returns.
                # A standard mock configured with return_value works for methods.
                return_value=known_org_payload # What the mocked org() method will return
                ) as mock_org_method: # The mock for the org method

            # Instantiate the client
            client_instance = GithubOrgClient("specific_org")

            # Access the _public_repos_url property.
            # This will internally call client_instance.org(), which is now mocked.
            actual_repos_url = client_instance._public_repos_url

            # Assert that the property returned the expected URL
            self.assertEqual(actual_repos_url, expected_repos_url_value)

            # Assert that our mock for the 'org' method was called once
            # by the _public_repos_url property's implementation.
            mock_org_method.assert_called_once()


# Ensure a single newline at the end of the file for Pycodestyle (W292)
# Remove if __name__ == '__main__': unittest.main() if not needed for ALX checker