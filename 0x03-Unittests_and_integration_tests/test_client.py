#!/usr/bin/env python3
""" Testing github """
import unittest
from unittest.mock import Mock, patch, PropertyMock, call
from parameterized import parameterized, parameterized_class
import utils
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ parameterize, patch org method, public repos """
    @parameterized.expand([
        ("google", {"google": True}),
        ("abc", {"abc": True})
    ])
    @patch('client.get_json')
    def test_org(self, org, expected_output, get_patch):
        """testing org method from client module """
        get_patch.return_value = expected_output
        git = GithubOrgClient(org)
        self.assertEqual(git.org, expected_output)
        get_patch.assert_called_once_with("https://api.github.com/orgs/"+org)

    def test_public_repos_url(self):
        """ test for the public urls """
        expected_output = "www.output.com"
        payload = {"repos_url": expected_output}
        mocked = 'client.GithubOrgClient.org'
        with patch(mocked, PropertyMock(return_value=payload)):
            cm = GithubOrgClient("git")
            self.assertEqual(cm._public_repos_url, expected_output)

    @patch('client.get_json')
    def test_public_repos(self, get_json_mock):
        """public repo testing """
        alex = {"name": "alex", "license": {"key": "a"}}
        renee = {"name": "renee", "license": {"key": "b"}}
        morgan = {"name": "morgan", }
        to_mock = 'client.GithubOrgClient._public_repos_url'
        get_json_mock.return_value = [alex, renee, morgan]

        with patch(to_mock, PropertyMock(return_value="www.output.com")) as r:
            git = GithubOrgClient("git")
            self.assertEqual(git.public_repos(), ['alex', 'renee', 'morgan'])
            self.assertEqual(git.public_repos("a"), ['alex'])
            self.assertEqual(git.public_repos("c"), [])
            self.assertEqual(git.public_repos(45), [])
            get_json_mock.assert_called_once_with("www.output.com")
            r.assert_called_once_with()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_licence(self, repo, license, expected):
        """ check licence availability """
        self.assertEqual(GithubOrgClient.has_license(repo, license), expected)