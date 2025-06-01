#!/usr/bin/env python3
"""
GitHub Organization Client
"""
from utils import get_json, memoize
from typing import Dict, Any, List, Union


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
        """
        url = self.ORG_URL.format(org=self._org_name)
        org_data = get_json(url)
        return org_data

    @property
    def _public_repos_url(self) -> str:
        """
        Returns the URL for the organization's public repositories.
        """
        org_data = self.org()
        return org_data.get("repos_url", "")

    def public_repos(self, license_key: Union[str, None] = None) -> List[str]:
        """
        Fetches and returns a list of public repository names for the org.
        Optionally filters by license_key using the has_license static method.
        """
        repos_url = self._public_repos_url
        if not repos_url:
            return []

        all_repos_payload = get_json(repos_url)
        repo_names: List[str] = []

        for repo in all_repos_payload:
            if isinstance(repo, dict):
                if license_key:
                    if self.has_license(repo, license_key): # Use the static method
                        repo_names.append(repo.get("name", ""))
                else:
                    repo_names.append(repo.get("name", ""))
        return repo_names

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """
        Checks if a repository dictionary contains a specific license key.

        Args:
            repo (Dict[str, Dict]): The repository dictionary, expected to have
                                    a 'license' key which is another dictionary
                                    containing a 'key' for the license.
            license_key (str): The license key string to check for (e.g., "mit", "apache-2.0").

        Returns:
            bool: True if the repo has the specified license_key, False otherwise.
                  Returns False if 'license' is not present or not a dict,
                  or if 'license' dict does not contain 'key'.
        """
        if not isinstance(repo, dict):
            return False # Or raise TypeError
        
        repo_license = repo.get("license")
        if not isinstance(repo_license, dict):
            return False
        
        return repo_license.get("key") == license_key

