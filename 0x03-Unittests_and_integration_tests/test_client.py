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
import requests


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
    def test_has_license(self, repo, license, expected):
        """ check license availability """
        self.assertEqual(GithubOrgClient.has_license(repo, license), expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ testing integration into github """

    @classmethod
    def setUpClass(cls):
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock

        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()

        option = {cls.org_payload["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: option.get(y, org_mock)

    @classmethod
    def tearDownClass(cls):
        """ tear down testing patcher """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ testing the public repos """
        git = GithubOrgClient("x")
        self.assertEqual(git.org, self.org_payload)
        self.assertEqual(git.repos_payload, self.repos_payload)
        self.assertEqual(git.public_repos(), self.expected_repos)
        self.assertEqual(git.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])

    def test_public_repos_with_license(self):
        """ public repos test """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.assertEqual(y.public_repos("apache-2.0"), self.apache2_repos)
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])
