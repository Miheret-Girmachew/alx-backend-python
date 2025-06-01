#!/usr/bin/env python3
"""
GitHub Organization Client
"""
from utils import get_json, memoize
from typing import Dict, Any, List, Union # Added Union


class GithubOrgClient:
    """
    A client for fetching information about GitHub organizations.
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """
        Initializes the client with the organization name.
        Args:
            org_name (str): The name of the GitHub organization.
        """
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """
        Fetches and returns the organization's information from GitHub API.
        Uses the ORG_URL template and calls get_json.
        The @memoize decorator will cache the result of this method.
        """
        url = self.ORG_URL.format(org=self._org_name)
        org_data = get_json(url)
        return org_data

    @property
    def _public_repos_url(self) -> str:
        """
        Returns the URL for the organization's public repositories.
        This is derived from the 'repos_url' field in the organization's data,
        obtained by calling the (potentially memoized) self.org() method.
        """
        org_data = self.org()
        return org_data.get("repos_url", "")

    def public_repos(self, license_key: Union[str, None] = None) -> List[str]:
        """
        Fetches and returns a list of public repository names for the org.
        Optionally filters by license_key.
        """
        # Get the URL for public repos from the property
        repos_url = self._public_repos_url # This is a property access
        if not repos_url:
            return []

        # Fetch the raw repo data from the repos_url
        # This get_json call will be mocked by the @patch decorator in the test
        all_repos_payload = get_json(repos_url)

        # Extract just the names, and filter by license if requested
        repo_names: List[str] = []
        for repo in all_repos_payload:
            if isinstance(repo, dict): # Ensure repo is a dictionary
                # License filtering logic
                if license_key:
                    repo_license = repo.get("license")
                    if isinstance(repo_license, dict) and repo_license.get("key") == license_key:
                        repo_names.append(repo.get("name", ""))
                else: # No license filter, add all repo names
                    repo_names.append(repo.get("name", ""))
        return repo_names


