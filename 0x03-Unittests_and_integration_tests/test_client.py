#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock, call  # Added call
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict, Any, List


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google",
         {"login": "google", "id": 1, "repos_url": "google_repos_url_payload"}),
        ("abc",
         {"login": "abc", "id": 2, "repos_url": "abc_repos_url_payload"}),
    ])
    @patch('client.get_json')
    def test_org(
            self,
            org_name: str,
            expected_org_payload: Dict,
            mock_get_json: Mock
            ) -> None:
        """Tests that `GithubOrgClient.org` returns the correct mocked payload."""
        mock_get_json.return_value = expected_org_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), expected_org_payload)
        expected_api_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_api_url)

    def test_public_repos_url(self) -> None:
        """
        Tests the `_public_repos_url` property by mocking `GithubOrgClient.org`.
        """
        known_org_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        with patch.object(
                GithubOrgClient,
                'org',
                return_value=known_org_payload
                ) as mock_org_method:
            client_instance = GithubOrgClient("testorg")
            actual_public_repos_url = client_instance._public_repos_url
            self.assertEqual(
                actual_public_repos_url,
                known_org_payload["repos_url"]
            )
            mock_org_method.assert_called_once()

    @parameterized.expand([
        (
            [{"name": "repo-alpha"}, {"name": "repo-beta"}],
            ["repo-alpha", "repo-beta"]
        ),
        (
            [{"name": "single-repo", "license": {"key": "mit"}}],
            ["single-repo"]
        ),
        (
            [],
            []
        ),
    ])
    @patch('client.get_json')
    def test_public_repos(
            self,
            repos_payload_from_api: List[Dict],
            expected_repo_names: List[str],
            mock_get_json: Mock
            ) -> None:
        """
        Tests `GithubOrgClient.public_repos` method.
        - Mocks `_public_repos_url` property to return a known URL.
        - Mocks `get_json` (called by `public_repos`) to return a known payload.
        - Verifies the returned list of repo names.
        - Verifies that mocks were called as expected.
        """
        client_instance = GithubOrgClient("some_org")
        mocked_repos_url_value = "https://api.github.com/orgs/some_org/repos"
        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock,
                return_value=mocked_repos_url_value
                ) as mock_public_repos_url_property:
            mock_get_json.return_value = repos_payload_from_api
            actual_repo_names = client_instance.public_repos()
            self.assertEqual(actual_repo_names, expected_repo_names)
            mock_public_repos_url_property.assert_called_once()
            mock_get_json.assert_called_once_with(mocked_repos_url_value)