#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client module.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
import fixtures
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct org info.
        """
        # Structure matches fixtures.org_payload
        mock_get_json.return_value = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        client_obj = GithubOrgClient(org_name)
        result = client_obj.org
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"})

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns correct URL.
        """
        repos_url = "https://api.github.com/orgs/google/repos"
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": repos_url}
            client_obj = GithubOrgClient("google")
            result = client_obj._public_repos_url
            self.assertEqual(result, repos_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns expected repo list.
        """
        # Use repo payload structure in fixtures
        mock_get_json.return_value = fixtures.repos_payload
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = fixtures.org_payload["repos_url"]
            client_obj = GithubOrgClient("google")
            result = client_obj.public_repos()
            self.assertEqual(result, fixtures.expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(fixtures.org_payload["repos_url"])

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "bsd-3-clause"}}, "apache-2.0", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that GithubOrgClient.has_license returns correct value.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class using real fixtures.
    """

    @classmethod
    def setUpClass(cls):
        """Mock requests.get with fixture payloads."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def get_url_side_effect(url):
            mock_response = Mock()
            # Match your fixture structure
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = get_url_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Assert full repo names match expected from fixtures."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Assert repos with apache2 license from fixtures."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )

if __name__ == "__main__":
    unittest.main()
