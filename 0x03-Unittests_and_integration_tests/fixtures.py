#!/usr/bin/env python3
"""
Test fixtures for GitHub Org Client integration tests.
"""

# Example org_payload (simplified)
# This payload should contain the 'repos_url' that will be used by _public_repos_url
ORG_PAYLOAD = {
    "google": {
        "login": "google",
        "id": 1342004,
        "repos_url": "https://api.github.com/orgs/google/repos", # Key URL
        "name": "Google"
    },
    "abc": { # Another org example for parameterization
        "login": "abc",
        "id": 123456,
        "repos_url": "https://api.github.com/orgs/abc/repos",
        "name": "Alphabet Inc."
    }
}

# Example repos_payload for a specific org (e.g., Google's repos_url)
# This is what get_json(repos_url) should return.
REPOS_PAYLOAD = {
    "google": [ # Corresponds to ORG_PAYLOAD["google"]["repos_url"]
        {"name": "episodes.dart", "license": {"key": "bsd-3-clause"}},
        {"name": "kratu", "license": {"key": "apache-2.0"}},
        {"name": "truth", "license": {"key": "apache-2.0"}},
        {"name": "ruby-openid-apps-discovery", "license": None}, # No license
        {"name": "dagger", "license": {"key": "apache-2.0"}},
    ],
    "abc": [ # Corresponds to ORG_PAYLOAD["abc"]["repos_url"]
        {"name": "abc-repo1", "license": {"key": "mit"}},
        {"name": "abc-repo2", "license": {"key": "apache-2.0"}},
        {"name": "abc-repo3", "license": None},
    ]
}

# Expected list of repo names (without license filter) for a specific org
EXPECTED_REPOS = {
    "google": ["episodes.dart", "kratu", "truth", "ruby-openid-apps-discovery", "dagger"],
    "abc": ["abc-repo1", "abc-repo2", "abc-repo3"]
}

# Expected list of repo names (filtered by "apache-2.0" license) for a specific org
APACHE2_REPOS = {
    "google": ["kratu", "truth", "dagger"],
    "abc": ["abc-repo2"]
}

# You might structure fixtures as a list of dictionaries for parameterized_class
# if you want to test multiple orgs in the integration test.
# Example:
# TEST_FIXTURES = [
#     {
#         "org_name": "google",
#         "org_payload": ORG_PAYLOAD["google"],
#         "repos_payload": REPOS_PAYLOAD["google"],
#         "expected_repos": EXPECTED_REPOS["google"],
#         "apache2_repos": APACHE2_REPOS["google"]
#     },
#     {
#         "org_name": "abc",
#         "org_payload": ORG_PAYLOAD["abc"],
#         "repos_payload": REPOS_PAYLOAD["abc"],
#         "expected_repos": EXPECTED_REPOS["abc"],
#         "apache2_repos": APACHE2_REPOS["abc"]
#     }
# ]