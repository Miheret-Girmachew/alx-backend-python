#!/usr/bin/env python3
"""
GitHub Organization Client
"""
# Ensure utils.py is in the same directory or python path
# For ALX, utils.py is often provided at the root of the task directory
from utils import get_json, memoize
from typing import Dict, Any, List # List was in your comment, keep if used


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
        # Removed self._org_payload instance variable as @memoize on org()
        # will handle caching. If @memoize caches on the instance (e.g., sets an
        # attribute like _memoized_org), that's fine.
        # If org() itself implements caching like you had with `if self._org_payload is None:`,
        # then @memoize might be redundant or needs to work with that.
        # For now, assuming @memoize handles the caching of org()'s result.

    @memoize # The result of this method will be cached by the decorator
    def org(self) -> Dict:
        """
        Fetches and returns the organization's information from GitHub API.
        Uses the ORG_URL template and calls get_json.
        The @memoize decorator will cache the result of this method.
        """
        url = self.ORG_URL.format(org=self._org_name)
        # The actual HTTP call happens here, which we will mock in tests
        org_data = get_json(url)
        return org_data

    @property
    def _public_repos_url(self) -> str:
        """
        Returns the URL for the organization's public repositories.
        This is derived from the 'repos_url' field in the organization's data,
        obtained by calling the (potentially memoized) self.org() method.
        """
        # Calling self.org() will return the (possibly cached) organization data
        org_data = self.org()
        # Assuming the payload from org() contains a 'repos_url' key
        return org_data.get("repos_url", "") # Return "" if key is missing

    # Example method that uses _public_repos_url (not tested in this task)
    # def public_repos(self, payload: bool = False) -> Union[List[str], List[Dict]]:
    #     """
    #     Fetches and returns a list of public repositories for the org.
    #     If payload is False, returns a list of repo names.
    #     If payload is True, returns the full list of repo dicts.
    #     (This is an example, adjust as needed)
    #     """
    #     repos_url = self._public_repos_url
    #     if not repos_url:
    #         return []
    #
    #     repos_list_payload = get_json(repos_url)
    #
    #     if payload:
    #         return repos_list_payload
    #     else:
    #         return [repo["name"] for repo in repos_list_payload]

# If you want to test client.py directly (makes actual HTTP calls)
# if __name__ == '__main__':
#     # Ensure utils.py with get_json and memoize is available
#     # and requests library is installed (pip install requests)
#     try:
#         google_client = GithubOrgClient("google")
#         print("Fetching Google org data...")
#         google_org_data = google_client.org() # First call to org, fetches and caches
#         print(f"Org Name: {google_org_data.get('login')}")
#         print(f"Public Repos URL: {google_client._public_repos_url}") # Uses cached org data
#
#         # Second call to org() should use memoized result
#         print("\nFetching Google org data again (should be memoized)...")
#         google_org_data_again = google_client.org()
#         print(f"Org Name (again): {google_org_data_again.get('login')}")
#
#     except Exception as e:
#         print(f"Error during example client.py usage: {e}")