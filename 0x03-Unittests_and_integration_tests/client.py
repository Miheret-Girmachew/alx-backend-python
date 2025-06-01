#!/usr/bin/env python3
"""
GitHub Organization Client
"""
# Assuming get_json is in utils.py and utils.py is in the same directory
# or accessible via PYTHONPATH.
from utils import get_json # Or wherever get_json is defined
from typing import Dict, Any

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

    def org(self) -> Dict:
        """
        Fetches and returns the organization's information from GitHub API.
        Uses the ORG_URL template and calls get_json.
        """
        url = self.ORG_URL.format(org=self._org_name)
        # This is the call we will mock in our tests
        org_data = get_json(url)
        return org_data

    # Other methods might exist here (e.g., for repos, members)
    # For this task, we only care about the .org() method.

if __name__ == '__main__':
    # Example Usage (would make actual HTTP calls if not mocked)
    # Ensure utils.py with get_json is available and requests is installed
    try:
        google_client = GithubOrgClient("google")
        print("Fetching Google org data (live call, will fail if requests not mocked/installed):")
        # print(google_client.org())
    except Exception as e:
        print(f"Error during example usage: {e}")