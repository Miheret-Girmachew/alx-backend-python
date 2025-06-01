#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock, call
from parameterized import parameterized, parameterized_class # If using parameterized_class later
# Ensure client.py is in the same directory or python path
from client import GithubOrgClient
from typing import Dict, Any, List
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google",
         {"login": "google", "id": 1, "repos_url": "google_url"}),
        ("abc",
         {"login": "abc", "id": 2, "repos_url": "abc_url"}),
    ])
    @patch('client.get_json')
    def test_org(
            self,
            org_name: str,
            expected_payload: Dict,
            mock_get_json: Mock
            ) -> None:
        """Tests that `GithubOrgClient.org` returns the correct mocked payload."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), expected_payload)
        expected_api_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_api_url)

    def test_public_repos_url(self) -> None:
        """
        Tests `_public_repos_url` property by mocking `GithubOrgClient.org`.
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
            actual_url = client_instance._public_repos_url
            self.assertEqual(
                actual_url,
                known_org_payload["repos_url"]
            )
            mock_org_method.assert_called_once()

    @parameterized.expand([
        (  # Test Case 1: Two repos in payload
            [{"name": "repo-alpha"}, {"name": "repo-beta"}],  # repos_payload
            ["repo-alpha", "repo-beta"]  # expected_names
        ),
        (  # Test Case 2: One repo in payload
            [{"name": "single-repo", "license": {"key": "mit"}}],
            ["single-repo"]
        ),
        (  # Test Case 3: Empty list of repos from API
            [],
            []
        ),
    ])
    @patch('client.get_json')
    def test_public_repos(
            self,
            repos_payload_from_api: List[Dict],
            expected_repo_names: List[str],
            mock_get_json_for_repos: Mock
            ) -> None:
        """
        Tests `GithubOrgClient.public_repos` method.
        Mocks `_public_repos_url` and `get_json` for repo list.
        """
        client_instance = GithubOrgClient("some_org_name")
        mocked_repos_url_value = "https://api.example.com/orgs/some_org/repos"

        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock,
                return_value=mocked_repos_url_value
                ) as mock_prop_repos_url:

            mock_get_json_for_repos.return_value = repos_payload_from_api
            actual_repo_names = client_instance.public_repos()
            self.assertEqual(actual_repo_names, expected_repo_names)
            mock_prop_repos_url.assert_called_once()
            mock_get_json_for_repos.assert_called_once_with(
                mocked_repos_url_value
            )

    # New test method for Task 7 (has_license)
    @parameterized.expand([
        # repo, license_key, expected_return_value
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": {"key": "my_license"}}, "other_license", False), # Added more cases
        ({"license": None}, "my_license", False),
        ({"no_license_key": True}, "my_license", False),
        ({}, "my_license", False), # Empty repo dict
        ({"license": {"not_key": "my_license"}}, "my_license", False) # License dict, but no 'key'
    ])
    def test_has_license(
            self,
            repo: Dict[str, Any],
            license_key: str,
            expected: bool
            ) -> None:
        """
        Tests the static method `GithubOrgClient.has_license`.

        Args:
            repo (Dict[str, Any]): The repository dictionary to check.
            license_key (str): The license key to look for.
            expected (bool): The expected boolean result.
        """
        # Call the static method directly using the class name
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide patch for requests.get."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Side effect function to return different payloads based on URL
        def get_side_effect(url):
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos filtered by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


