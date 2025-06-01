#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock, call # Added call
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict, Any, List


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1, "repos_url": "google_repos_url_payload"}),
        ("abc", {"login": "abc", "id": 2, "repos_url": "abc_repos_url_payload"}),
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
        # Case 1: Test with a specific license
        (
            {"license": {"key": "my_license"}}, # Mocked _public_repos_url payload
            "my_license", # license_key argument for public_repos
            [ # Expected repo names
                {"name": "repo1", "license": {"key": "my_license"}},
                {"name": "repo2", "license": {"key": "other_license"}},
                {"name": "repo3", "license": {"key": "my_license"}},
            ],
            ["repo1", "repo3"] # Expected result from public_repos
        ),
        # Case 2: Test without a specific license (all repos)
        (
            {"license": {"key": "apache-2.0"}}, # This payload part is for _public_repos_url mock, not directly used by this test logic for selection
            None, # No license_key argument for public_repos
            [ # Mocked payload for get_json(repos_url)
                {"name": "free-repo", "license": {"key": "mit"}},
                {"name": "another-repo", "license": {"key": "gpl"}},
            ],
            ["free-repo", "another-repo"] # Expected result from public_repos
        ),
    ])
    @patch('client.get_json') # This will mock get_json called by public_repos
    def test_public_repos(
            self,
            # Parameters from parameterized.expand for _public_repos_url mocking (if needed, though we mock it directly)
            # For this test, we directly control _public_repos_url, so these aren't strictly used for its setup.
            # Let's re-think the parameters for this specific test as per instruction.
            # The instruction is:
            # 1. Use @patch as a decorator to mock get_json and make it return a payload of your choice (for repos).
            # 2. Use patch as a context manager to mock GithubOrgClient._public_repos_url and return a value of your choice.
            # So, parameterized should give us the known_repos_payload (for get_json) and expected_repo_names.
            # We also need a license_key for one test case.
            # Let's redefine parameters for parameterized.expand more directly.
            # Parameter set: (license_key_arg, mock_repos_payload, expected_repo_names_list)
            # The first test_case in the instructions for previous task did not use license filtering
            # but it's a good way to show conditional logic within public_repos.
            # For this task, let's simplify to just test the list of repos.
            
            # New parameterization:
            # (repos_payload_for_get_json, expected_list_of_names)
            # This aligns with "make it return a payload of your choice" for get_json.
            # And "Test that the list of repos is what you expect from the chosen payload."

            # Simplified parameterization based on direct instructions:
            # We need a payload for the mocked get_json(repos_url) call
            # And we need the expected list of repo names.
            # The _public_repos_url will be mocked to a fixed value inside the test.

            # Let's make parameterized provide the repos_payload that get_json(repos_url) will return.
            # And the expected list of names derived from that payload.
            # We will test with two different repo payloads.
            # Example test_payload_for_repos and expected_repo_names
            # (test_case_name_for_clarity, repos_payload, expected_names) # Not using test_case_name
            repos_payload_from_api: List[Dict], # What get_json(repos_url) will return
            expected_repo_names: List[str],
            mock_get_json: Mock # Injected by @patch('client.get_json')
            ) -> None:
        """
        Tests `GithubOrgClient.public_repos` method.
        - Mocks `_public_repos_url` property to return a known URL.
        - Mocks `get_json` (called by `public_repos`) to return a known payload of repos.
        - Verifies the returned list of repo names.
        - Verifies that mocks were called as expected.
        """
        # The org name used to instantiate client doesn't matter much here
        # as _public_repos_url will be mocked.
        client_instance = GithubOrgClient("some_org")

        # 1. Mock `_public_repos_url` property using patch as a context manager.
        #    It should return a chosen URL value.
        mocked_repos_url_value = "https://api.github.com/orgs/some_org/repos"
        with patch.object(
                GithubOrgClient,
                '_public_repos_url', # Name of the property to patch
                new_callable=PropertyMock, # Use PropertyMock for @property
                return_value=mocked_repos_url_value
                ) as mock_public_repos_url_property:

            # 2. Configure the @patched `mock_get_json`.
            #    This mock is for the get_json call made *inside* public_repos
            #    when it tries to fetch from `mocked_repos_url_value`.
            #    The `repos_payload_from_api` comes from @parameterized.expand.
            mock_get_json.return_value = repos_payload_from_api

            # Call the method under test
            actual_repo_names = client_instance.public_repos()

            # 3. Test that the list of repos is what you expect
            self.assertEqual(actual_repo_names, expected_repo_names)

            # 4. Test that the mocked property (_public_repos_url) was called once.
            mock_public_repos_url_property.assert_called_once()

            # 5. Test that the mocked get_json was called once with the URL
            #    that _public_repos_url was mocked to return.
            mock_get_json.assert_called_once_with(mocked_repos_url_value)

# Re-doing the parameterization for test_public_repos for clarity
# to provide (repos_payload_for_get_json, expected_list_of_names)
TestGithubOrgClient.test_public_repos = parameterized.expand([
    ( # Test Case 1: Two repos
        [{"name": "repo-alpha"}, {"name": "repo-beta"}], # Payload for get_json(repos_url)
        ["repo-alpha", "repo-beta"] # Expected names
    ),
    ( # Test Case 2: One repo
        [{"name": "single-repo", "license": {"key": "mit"}}], # Payload for get_json(repos_url)
        ["single-repo"] # Expected names
    ),
    ( # Test Case 3: Empty list of repos from API
        [], # Payload for get_json(repos_url)
        []  # Expected names
    ),
])(TestGithubOrgClient.test_public_repos)


# Ensure single newline at end of file